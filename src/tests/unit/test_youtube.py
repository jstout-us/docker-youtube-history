# -*- coding: utf-8 -*-

"""Test module doc string."""
import json
from pathlib import Path
from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

from app import youtube
from app.exceptions import EmptyResponseError


@pytest.fixture
def fix_empty_resp():
    with Path('src/tests/_fixtures/files/youtube_empty_response.json').open() as fd_in:
        fixture = json.load(fd_in)

    return fixture


@pytest.fixture
def fix_valid_resp():
    with Path('src/tests/_fixtures/files/youtube_valid_response.json').open() as fd_in:
        fixture = json.load(fd_in)

    return fixture


def test_get(fix_auth_token, fix_empty_resp, fix_valid_resp):
    with patch('app.youtube._get_youtube') as mock_get_yt:
        mock_get_yt.side_effect = [fix_valid_resp, fix_empty_resp]

        assert youtube.get('token', 'type', 'id')

        with pytest.raises(EmptyResponseError):
            youtube.get('token', 'type', 'id')


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


def test_refresh_token():
    token_mock = MagicMock()
    token_mock.expired = False
    token_mock.refresh_token = False
    token_mock.refresh = MagicMock()

    token_mock = youtube.refresh_token(token_mock)

    token_mock.expired = True
    token_mock = youtube.refresh_token(token_mock)

    token_mock.refresh_token = True
    token_mock = youtube.refresh_token(token_mock)

    token_mock.refresh.assert_called_once()
