# -*- coding: utf-8 -*-

"""Test module doc string."""
from unittest.mock import MagicMock

import pytest

from app.youtube import _parse_url_tag
from app.youtube import _parse_watched


def test_parse_url_tag():
    expect_chan_id = 'c_1'
    expect_chan_title = 'Channel 1'

    expect_vid_id = 'v_1'
    expect_vid_title = 'Video 1'

    url_tag = MagicMock
    url_tag.attrs = {'href': 'https://www.youtube.com/channel/{}'.format(expect_chan_id)}
    url_tag.contents = [expect_chan_title]

    id_, title = _parse_url_tag(MagicMock)

    assert expect_chan_id == id_
    assert expect_chan_title == title


    url_tag = MagicMock
    url_tag.attrs = {'href': 'https://www.youtube.com/watch?v={}'.format(expect_vid_id)}
    url_tag.contents = [expect_vid_title]

    id_, title = _parse_url_tag(MagicMock)

    assert expect_vid_id == id_
    assert expect_vid_title == title


def test_parse_watched():
    txt = """
    <div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">
     Watched
     <a href="https://www.youtube.com/watch?v=v_1">
      Video 1
     </a>
     <br/>
     <a href="https://www.youtube.com/channel/c_1">
      Channel 1
     </a>
     <br/>
     Jan 01, 1970, 8:00:00 AM EDT
    </div>
    """
    txt = "May 28, 2019, 4:19:04 PM EDT"
    # expect = '1970-01-01T12:00:00Z'
    expect = '2019-05-28T20:19:04Z'
    watched = _parse_watched(txt)

    assert expect == watched


# def test_parse_tag():
    """
    Three possible scenarios:
    1.  deleted (no urls)
    2.  orphaned video (one url)
    3.  normal (two urls)
    """


    # tag_channel_a.attrs['href']
    # tag_channel_a.contents[0]
    # urls = [

    #     ]
