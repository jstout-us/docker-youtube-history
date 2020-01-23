# -*- coding: utf-8 -*-

"""Test module doc string."""
import json
import pickle
from datetime import datetime

import pytest

from app import util


@pytest.fixture
def exp_data():
    expected = {
        'one': 1,
        'two': 2
        }

    return expected


def test_get_sleep_time():
    time_now = datetime(1970, 1, 1, 12, 1, 0)
    time_start = datetime(1970, 1, 1, 12, 0, 0)

    expected = 60
    result = util.get_sleep_time(time_start, time_now, 120)
    assert expected == result

    expected = 0
    result = util.get_sleep_time(time_start, time_now, 0)
    assert expected == result


def test_load_pickle_file(tmp_path, exp_data):
    file_path = tmp_path / 'test.pkl'

    with pytest.raises(FileNotFoundError):
        util.load_file(file_path)

    with file_path.open('wb') as fd_out:
        pickle.dump(exp_data, fd_out)

    result = util.load_file(file_path)
    assert exp_data == result


def test_load_json_file(tmp_path, exp_data):
    file_path = tmp_path / 'test.json'

    with pytest.raises(FileNotFoundError):
        util.load_file(file_path)

    with file_path.open('w') as fd_out:
        json.dump(exp_data, fd_out)

    result = util.load_file(file_path)
    assert exp_data == result


def test_save_pickle_file(tmp_path, exp_data):
    file_path = tmp_path / 'test.pkl'

    util.save_file(file_path, exp_data)

    with file_path.open('rb') as fd_in:
        result = pickle.load(fd_in)

    assert exp_data == result


def test_save_json_file(tmp_path, exp_data):
    file_path = tmp_path / 'test.json'

    util.save_file(file_path, exp_data)

    with file_path.open() as fd_in:
        result = json.load(fd_in)

    assert exp_data == result
