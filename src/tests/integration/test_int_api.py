# -*- coding: utf-8 -*-

"""Test module doc string."""
import json
import pickle
from pathlib import Path
from unittest.mock import patch

import pytest

from app import api
from app import settings
from app.exceptions import NotAuthenticatedError


def test_load_tasks(tmp_path, fix_task_list):
    config = {
        'file_history': Path('src/tests/_fixtures/files/watch-history.html'),
        'file_task_queue': tmp_path / 'task.queue'
        }

    with patch.dict(settings.config, config):
        tasks = api.load_tasks()

        queue = []
        with config['file_task_queue'].open() as fd_in:
            for line in fd_in:
                queue.append(json.loads(line))

        assert expected_tasks == tasks
        assert expected_queue == queue

        # Verify existing file not overwritten
        queue_stat = config['file_task_queue'].stat()
        api.load_tasks()
        assert queue_stat == config['file_task_queue'].stat()


def test_setup(tmp_path):

    dir_root = tmp_path
    dir_in = dir_root / 'in'
    dir_out = dir_root / 'out'
    dir_work = dir_root / 'work'
    dir_work_data = dir_work / 'data'
    dir_work_var = dir_work / 'var'

    expected_config = {
        'api_poll_int': 120,
        'dir_in': dir_in,
        'dir_out': dir_out,
        'dir_work': dir_work,
        'dir_work_data': dir_work_data,
        'dir_work_var': dir_work_var,
        'file_token': dir_work_var / 'token.pkl',
        'file_history': dir_in / 'watch-history.html',
        'file_log': dir_work / 'run.log',
        'file_task_queue': dir_work_var / 'task.queue'
        }

    api.setup(dir=dir_root)

    assert expected_config == settings.config
    assert expected_config['dir_work_data'].is_dir()
    assert expected_config['dir_work_var'].is_dir()


def test_test_auth(tmp_path):
    file_token = tmp_path / 'token.pkl'

    with patch.dict(settings.config, {'file_token': file_token}):
        with pytest.raises(NotAuthenticatedError):
            api.test_auth()

        with file_token.open('wb') as fd_out:
            pickle.dump({'one': 1}, fd_out)

        api.test_auth()
