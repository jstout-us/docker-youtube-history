# -*- coding: utf-8 -*-

"""Test module doc string."""
import pickle
from datetime import datetime
import pytest

from app import util


def test_get_sleep_time():
    time_now = datetime(1970, 1, 1, 12, 1, 0)
    time_start = datetime(1970, 1, 1, 12, 0, 0)

    expected = 60
    result = util.get_sleep_time(time_start, time_now, 120)
    assert expected == result

    expected = 0
    result = util.get_sleep_time(time_start, time_now, 0)
    assert expected == result


def test_load_file(tmp_path):
    expected = {
        'one': 1,
        'two': 2
        }

    file_path = tmp_path / 'test.pkl'

    with pytest.raises(FileNotFoundError):
        util.load_file(file_path)

    with file_path.open('wb') as fd_out:
        pickle.dump(expected, fd_out)

    result = util.load_file(file_path)
    assert expected == result


def test_save_file(tmp_path):
    expected = {
        'one': 1,
        'two': 2
        }

    file_path = tmp_path / 'test.pkl'

    util.save_file(file_path, expected)

    with file_path.open('rb') as fd_in:
        result = pickle.load(fd_in)

    assert expected == result
