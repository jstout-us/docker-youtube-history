# -*- coding: utf-8 -*-

"""Module app.youtube."""
import os
from urllib.parse import urlparse

import googleapiclient.discovery
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from dateutil import parser
from dateutil import tz
from google.auth.transport import requests

from .exceptions import EmptyResponseError

MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
TIMEZONES = {
    'EDT': 'US/Eastern',
    'EST': 'US/Eastern'
    }


def _get_youtube(token, kind, id_):
    """Retreive record from Youtube via API.

    Args:
        token(Token):       Valid youtube auth token
        kind(str):          Type of record to retreive (channel, video)
        id_(str):           Record id field

    Raises:
        KeyError:           unknown type

    Returns:
        response(dict):     Youtube API response
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    api = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=token)

    if kind == 'channel':
        part = "id,contentDetails,contentOwnerDetails,statistics,topicDetails,status,snippet"
        request = api.channels().list(part=part, id=id_)   # pylint: disable=no-member

    elif kind == 'video':
        part = "contentDetails,id,localizations,recordingDetails,snippet"
        part += ",statistics,status,topicDetails"
        request = api.videos().list(part=part, id=id_)   # pylint: disable=no-member

    else:
        raise KeyError

    response = request.execute()

    return response


def _parse_url_tag(tag):
    result = urlparse(tag.attrs['href'])

    if result.query:
        id_ = result.query.split('=')[-1]

    else:
        id_ = result.path.split('/')[-1]

    title = tag.contents[0].strip()

    return (id_, title)


def _parse_watched(text):
    text = text.replace('\n', '').rstrip()
    idx_left = sorted([x for x in [text.rfind(y) for y in MONTHS_SHORT] if x > -1],
                      reverse=True)[0]
    idx_right = text.rfind(' ')

    tz_ = TIMEZONES[text[idx_right:].strip()]
    watched = parser.parse(text[idx_left:idx_right]).replace(tzinfo=tz.gettz(tz_))

    return watched.astimezone(tz.UTC).isoformat().replace('+00:00', 'Z')


def get(token, kind, id_):
    """Retreive record from Youtube via API.

    Args:
        token(Token):       Valid youtube auth token
        kind(str):          Type of record to retreive (channel, video)
        id_(str):           Record id field

    Raises:
        EmptyResponseError: No records returned from Youtube API

    Returns:
        response(dict):     Youtube API response
    """
    result = _get_youtube(token, kind, id_)

    if not result['pageInfo']['totalResults']:
        raise EmptyResponseError

    return result


def parse_history(path):
    """Parse youtube watched-history.html.

    Args:
        path(Path):     path to watched-history file

    Returns:
        videos(list):   List of video dictionaries.
    """
    videos = []

    kwargs = {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}
    only_vid_data = SoupStrainer(**kwargs)

    soup = BeautifulSoup(path.open().read(), "html.parser", parse_only=only_vid_data)

    for tag in soup:
        data = {}
        url_tags = tag.find_all('a')

        try:
            data['vid_id'], data['vid_title'] = _parse_url_tag(url_tags[0])
            data['watched'] = _parse_watched(tag.text)
            data['chan_id'], data['chan_title'] = _parse_url_tag(url_tags[1])

        except IndexError:
            data['chan_id'], data['chan_title'] = None, None

        if 'vid_id' in data:
            videos.append(data)

    return videos


def refresh_token(token):
    """Check token status and refresh if required.

    Args:
        token(Token):   Google auth token

    Returns
        token(Token):   Refreshed google token
    """
    if token.expired and token.refresh_token:
        token.refresh(requests.Request())

    return token
