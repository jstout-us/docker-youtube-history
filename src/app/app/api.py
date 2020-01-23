# -*- coding: utf-8 -*-

"""Module app.api."""
import collections
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


def export():
    """Archive run results to /out directory."""
    base_name = '{}/{}_youtube_import'.format(config['dir_out'], util.get_file_timestamp())

    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_stage = tmp_dir + '/work'
        shutil.copytree(str(config['dir_work']), dir_stage)
        os.unlink(tmp_dir + '/work/var/token.pkl')
        shutil.make_archive(base_name, 'zip', tmp_dir)


def load_tasks():
    """Load tasks from task queue or generated from watched-history.html.

    Returns:
        tasks(list):    List of task dictionaries
    """
    try:
        tasks = task_queue.load(config['file_task_queue'])

    except FileNotFoundError:
        videos = youtube.parse_history(config['file_history'])
        tasks = task_queue.create_tasks(videos)
        task_queue.save(config['file_task_queue'], *tasks)

    return tasks


def run(tasks):
    """Run tasks.

    Args:
        tasks(list):    Task objects

    Returns:
        None
    """
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

        except Exception:   # pylint: disable=broad-except
            pass

        finally:
            task_queue.save(config['file_task_queue'], task)

        time_sleep = util.get_sleep_time(time_start, datetime.now(), config['api_poll_int'])
        time.sleep(time_sleep)


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
        'file_log': dir_work / 'run.log',
        'file_task_queue': dir_work_var / 'task.queue'
        }

    cfg_update['dir_work_data'].mkdir(parents=True, exist_ok=True)
    cfg_update['dir_work_var'].mkdir(parents=True, exist_ok=True)

    config.update(cfg_update)


def test_auth():
    """Load token file to verify authecation status.

    Raises:
        NotAuthenticatedError:  Authentication token not found.
    """
    try:
        util.load_file(config['file_token'])

    except FileNotFoundError:
        raise NotAuthenticatedError
