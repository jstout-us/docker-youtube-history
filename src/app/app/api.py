# -*- coding: utf-8 -*-

"""Module app.api."""
from pathlib import Path

from . import settings
from . import util
from .exceptions import NotAuthenticatedError

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

    settings.config.update(cfg_update)


def test_auth():
    try:
        util.load_file(settings.config['file_token'])

    except FileNotFoundError:
        raise NotAuthenticatedError
