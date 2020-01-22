# -*- coding: utf-8 -*-

"""Test module doc string."""
from unittest.mock import MagicMock

import pytest

from app import youtube


def test_parse_url_tag():
    expect_chan_id = 'c_1'
    expect_chan_title = 'Channel 1'

    expect_vid_id = 'v_1'
    expect_vid_title = 'Video 1'

    url_tag = MagicMock
    url_tag.attrs = {'href': 'https://www.youtube.com/channel/{}'.format(expect_chan_id)}
    url_tag.contents = [expect_chan_title]

    id_, title = youtube._parse_url_tag(MagicMock)

    assert expect_chan_id == id_
    assert expect_chan_title == title


    url_tag = MagicMock
    url_tag.attrs = {'href': 'https://www.youtube.com/watch?v={}'.format(expect_vid_id)}
    url_tag.contents = [expect_vid_title]

    id_, title = youtube._parse_url_tag(MagicMock)

    assert expect_vid_id == id_
    assert expect_vid_title == title


def test_parse_watched():
    txt = """

     Watched

      Video 1



      Channel 1


     Jan 01, 1970, 7:00:00 AM EST

    """
    expect = '1970-01-01T12:00:00Z'
    result = youtube._parse_watched(txt)

    assert expect == result
