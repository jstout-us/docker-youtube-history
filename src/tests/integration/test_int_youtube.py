# -*- coding: utf-8 -*-

"""Test module doc string."""
from pathlib import Path

import pytest

from app.youtube import parse_history

from pprint import pprint as pp

@pytest.fixture
def exp_videos():
    expected = [
    {
        'chan_id': 'c_1',
        'chan_title': 'Channel 1',
        'vid_id': 'v_2',
        'vid_title': 'Video 2',
        'watched': '1970-02-01T12:00:00Z'
        },
    {
        'chan_id': 'c_2',
        'chan_title': 'Channel 2',
        'vid_id': 'v_3',
        'vid_title': 'Video 3',
        'watched': '1970-03-01T12:00:00Z'
        },
    {
        'chan_id': None,
        'chan_title': None,
        'vid_id': 'v_4',
        'vid_title': 'Video 4',
        'watched': '1970-04-01T12:00:00Z'
        },
    {
        'chan_id': 'c_1',
        'chan_title': 'Channel 1',
        'vid_id': 'v_1',
        'vid_title': 'Video 1',
        'watched': '1970-05-01T12:00:00Z'
        },
    ]

    return expected


@pytest.fixture
def exp_stats(exp_videos):
    expected = {
        'time_first': exp_videos[0]['watched'],
        'time_last': exp_videos[-1]['watched'],
        'total': 5,
        'orphaned': 1,
        'unique': 4,
        'duplicates': 1,
        'deleted': 1
        }

    return expected


@pytest.fixture
def fix_history():
    return Path('src/tests/_fixtures/files/watch-history.html')


def test_parse_yt_history(exp_videos, exp_stats, fix_history):

    videos, stats = parse_history(fix_history)

    assert exp_videos == videos
    assert exp_stats == stats
