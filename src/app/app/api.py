# -*- coding: utf-8 -*-

"""Module app.api."""
import collections
import logging
import os
import tempfile
import shutil
import time
from pathlib import Path
from datetime import datetime

from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError

from . import task_queue
from . import util
from . import youtube
from .exceptions import EmptyResponseError
from .exceptions import NotAuthenticatedError
from .settings import config
from .settings import LOG_FILE_MSG_FORMAT
from .settings import LOG_FILE_TIME_FORMAT
from .settings import LOG_STREAM_MSG_FORMAT
from .settings import LOG_STREAM_TIME_FORMAT

logger = logging.getLogger(__name__)    # pylint: disable=invalid-name


def export():
    """Archive run results to /out directory."""
    logger.debug('export() - enter')
    base_name = '{}/{}_youtube_import'.format(config['dir_out'], util.get_file_timestamp())

    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_stage = tmp_dir + '/work'
        shutil.copytree(str(config['dir_work']), dir_stage)
        os.unlink(tmp_dir + '/work/var/token.pkl')
        shutil.make_archive(base_name, 'zip', tmp_dir)

    logger.debug('export() - exit')


def load_tasks():
    """Load tasks from task queue or generated from watched-history.html.

    Returns:
        tasks(list):    List of task dictionaries
    """
    logger.debug('load_tasks() - enter')

    try:
        tasks = task_queue.load(config['file_task_queue'])
        logger.info('Found existing task.queue file. Loading cached tasks')

    except FileNotFoundError:
        logger.info('Task.queue file not found, parsing watch-history.html')
        videos = youtube.parse_history(config['file_history'])
        tasks = task_queue.create_tasks(videos)
        task_queue.save(config['file_task_queue'], *tasks)

    logger.info('Loaded %s tasks', len(tasks))
    logger.debug('load_tasks() - exit')

    return tasks


def run(tasks):
    """Run tasks.

    Args:
        tasks(list):    Task objects

    Returns:
        None
    """
    logger.debug('run() - enter')
    msg = 'YT Get - Result: %s Tasks Remaining: %s Time Remaining: %s'
    queue = collections.deque(tasks)

    while queue:
        time_start = datetime.now()
        task = queue.pop().copy()
        task['retry'] -= 1

        try:
            token = util.load_file(config['file_token'])
            token = youtube.refresh_token(token)
            util.save_file(config['file_token'], token)

            result = youtube.get(token, task['kind'], task['id'])
            task['state'] = 'ok'

            file_name = '{}_result.json'.format(util.get_file_timestamp())
            util.save_file(config['dir_work_data'] / file_name, result)

        except (EmptyResponseError, HttpError, NotAuthenticatedError, ServerNotFoundError):
            if task['retry']:
                task['state'] = 'error'
                queue.appendleft(task)

            else:
                task['state'] = 'failed'

        except Exception as exp:   # pylint: disable=broad-except
            task['state'] = 'error'
            logger.critical(exp, exc_info=True)

        finally:
            task_remain = len(queue)
            logger.info(msg, task['state'].upper(), task_remain,
                        util.get_time_remaining(task_remain, config['api_poll_int']))

            task_queue.save(config['file_task_queue'], task)

        time_sleep = util.get_sleep_time(time_start, datetime.now(), config['api_poll_int'])
        time.sleep(time_sleep)

    logger.debug('run() - exit')


def setup(**kwargs):
    """Configure app.

    Kwargs:
        dir(Path):  Overide default root path.

    Returns:
        None
    """
    dir_root = kwargs.get('dir', Path('/data'))
    dir_in = dir_root / 'in'
    dir_work = dir_root / 'work'
    dir_work_var = dir_work / 'var'

    cfg_update = {
        'api_poll_int': 120,
        'dir_in': dir_in,
        'dir_out': dir_root / 'out',
        'dir_work': dir_work,
        'dir_work_data': dir_work / 'data',
        'dir_work_var': dir_work_var,
        'file_token': dir_work_var / 'token.pkl',
        'file_history': dir_in / 'watch-history.html',
        'file_log': dir_work_var / 'run.log',
        'file_task_queue': dir_work_var / 'task.queue'
        }

    cfg_update['dir_work_var'].mkdir(parents=True, exist_ok=True)

    try:
        cfg_update['dir_work_data'].mkdir(parents=True)

    except FileExistsError:
        for path in [x for x in cfg_update['dir_work_data'].glob('*')]:
            path.unlink()

    config.update(cfg_update)

    try:
        shutil.copy(str(config['dir_in'] / 'token.pkl'), str(config['file_token']))

    except FileNotFoundError:
        pass

    logging.basicConfig(
        filename=config['file_log'],
        filemode='w',
        level=logging.DEBUG,
        format=LOG_FILE_MSG_FORMAT,
        datefmt=LOG_FILE_TIME_FORMAT
        )

    logging.getLogger()
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(LOG_STREAM_MSG_FORMAT, datefmt=LOG_STREAM_TIME_FORMAT)
        )
    logger.addHandler(handler)

    logger.info('Setup complete')
    logger.debug('setup() - exit')


def test_auth():
    """Load token file to verify authecation status.

    Raises:
        NotAuthenticatedError:  Authentication token not found.
    """
    try:
        util.load_file(config['file_token'])

    except FileNotFoundError:
        raise NotAuthenticatedError
