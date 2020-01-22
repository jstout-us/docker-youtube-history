# -*- coding: utf-8 -*-

"""Test module doc string."""
import pickle

import pytest

from app import util


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
