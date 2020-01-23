# -*- coding: utf-8 -*-

"""Test module doc string."""
import json
import pickle
from pathlib import Path
from unittest.mock import patch

import pytest

import app
from app import api
from app import settings
from app.exceptions import NotAuthenticatedError


@pytest.fixture
def fix_timestamp():
    return '1980-01-01T00:00:00Z'


@pytest.fixture
def fix_run_tasks(fix_task_list, fix_timestamp):
    tasks = [x.copy() for x in fix_task_list[-3:]]

    updates = [
        {},
        {'state': 'error', 'retry': 4},
        {'state': 'error', 'retry': 1},
        ]

    for task, update in zip(tasks, updates):
        task.update(update)

    return tasks


@pytest.fixture
def fix_run_results(fix_task_list, fix_timestamp):
    tasks = [x.copy() for x in fix_task_list[-3:]]
    tasks.reverse()
    tasks.append(fix_task_list[-2].copy())

    updates = [
        {'state': 'failed', 'retry': 0, 'timestamp': fix_timestamp},
        {'state': 'error', 'retry': 3, 'timestamp': fix_timestamp},
        {'state': 'ok', 'retry': 4, 'timestamp': fix_timestamp},
        {'state': 'ok', 'retry': 2, 'timestamp': fix_timestamp}
        ]

    for task, update in zip(tasks, updates):
        task.update(update)

    return tasks


def test_load_tasks(tmp_path, fix_task_list):
    config = {
        'file_history': Path('src/tests/_fixtures/files/watch-history.html'),
        'file_task_queue': tmp_path / 'task.queue'
        }

    with patch.dict(settings.config, config):
        with patch('app.util.get_timestamp_utc') as mock_f:
            mock_f.return_value = '1970-01-01T00:00:00Z'
            tasks = api.load_tasks()

            queue = []
            with config['file_task_queue'].open() as fd_in:
                for line in fd_in:
                    queue.append(json.loads(line))

            assert fix_task_list == tasks

            # Verify existing file not overwritten
            queue_stat = config['file_task_queue'].stat()
            api.load_tasks()
            assert queue_stat == config['file_task_queue'].stat()


@patch('app.youtube._get_youtube')
@patch('app.util.get_timestamp_utc')
def test_run(ts_mock, yt_mock, tmp_path, fix_run_tasks, fix_run_results, fix_auth_token,
             fix_yt_empty_resp, fix_yt_valid_resp):
    assert yt_mock is app.youtube._get_youtube
    assert ts_mock is app.util.get_timestamp_utc

    ts_mock.return_value = '1980-01-01T00:00:00Z'
    yt_mock.side_effect = [fix_yt_empty_resp, fix_yt_empty_resp, fix_yt_valid_resp,
                           fix_yt_valid_resp]

    dir_work_data = tmp_path / 'data'
    dir_work_data.mkdir()

    config = {
        'api_poll_int': 0,
        'dir_work_data': dir_work_data,
        'file_task_queue': tmp_path / 'task.queue',
        'file_token': tmp_path / 'token.pkl'
        }

    with config['file_token'].open('wb') as fd_out:
        pickle.dump(fix_auth_token, fd_out)

    with patch.dict(settings.config, config):
        api.run(fix_run_tasks)

        results = []
        with config['file_task_queue'].open() as fd_in:
            for line in fd_in:
                results.append(json.loads(line))


        assert fix_run_results == results
        assert (config['dir_work_data'] / '19800101_000000_result.json').is_file()
        assert (config['dir_work_data'] / '19800101_010000_result.json').is_file()


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
