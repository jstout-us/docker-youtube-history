# -*- coding: utf-8 -*-

"""Youtube module."""
import logging
from collections import defaultdict
from collections import OrderedDict
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from dateutil import parser
from dateutil import tz

logging.getLogger('foo').addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)    # pylint: disable=invalid-name

MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
TIMEZONES = {
    'EDT': 'US/Eastern',
    'EST': 'US/Eastern'
    }


class DeletedVideoError(Exception):
    """Exception raised for deleted videos."""


def _filter_unique(videos):
    unique = OrderedDict()

    for video in videos:
        unique[video['vid_id']] = video

    return list(unique.values())


def _parse_url_tag(tag):
    logger.debug('_parse_url_tag() - enter')

    result = urlparse(tag.attrs['href'])

    if result.query:
        id_ = result.query.split('=')[-1]

    else:
        id_ = result.path.split('/')[-1]

    title = tag.contents[0].strip()

    logger.debug('_parse_url_tag() - exit')
    return (id_, title)


def _parse_watched(txt):
    logger.debug('_parse_watched() - enter')

    txt = txt.replace('\n', '').rstrip()
    idx_left = sorted([x for x in [txt.rfind(y) for y in MONTHS_SHORT] if x > -1],
                      reverse=True)[0]
    idx_right = txt.rfind(' ')

    tz_ = TIMEZONES[txt[idx_right:].strip()]
    watched = parser.parse(txt[idx_left:idx_right]).replace(tzinfo=tz.gettz(tz_))

    logger.debug('_parse_watched() - exit')
    return watched.astimezone(tz.UTC).isoformat().replace('+00:00', 'Z')


def _parse_tag(tag):
    """Parse watch-history video element.

    Args:
        elem(str):  html formatted <div>

    Raises:
        DeletedVideoError:  Video has been deleted

    Returns:
        data(dict): Video data
    """
    logger.debug('_parse_tag() - enter')

    data = {}
    url_tags = tag.find_all('a')

    if not url_tags:
        raise DeletedVideoError

    try:
        data['vid_id'], data['vid_title'] = _parse_url_tag(url_tags[0])
        data['watched'] = _parse_watched(tag.text)
        data['chan_id'], data['chan_title'] = _parse_url_tag(url_tags[1])

    except IndexError:
        data['chan_id'], data['chan_title'] = None, None
        logger.debug('orphaned video - id: %s title: %s', data['vid_id'], data['vid_title'])

    logger.debug('_parse_tag() - exit')

    return data


def parse_history(path):
    """Parse watch-history.html.

    Args:
        path(Path): path to input file.

    Returns:
        videos(list):   List of video info dicts
        stats(dict):    Dictionary of watch history statistics
    """
    videos = []
    stats = defaultdict(int)

    kwargs = {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}
    only_vid_data = SoupStrainer(**kwargs)

    soup = BeautifulSoup(path.open().read(), "html.parser", parse_only=only_vid_data)

    for tag in soup:
        try:
            videos.append(_parse_tag(tag))

        except DeletedVideoError:
            stats['deleted'] += 1

    stats['total'] = len(videos)
    videos = _filter_unique(videos)
    videos.sort(key=lambda x: parser.parse(x['watched']))
    stats['orphaned'] = sum(1 for x in videos if not x['chan_id'])
    stats['unique'] = len(videos)
    stats['duplicates'] = stats['total'] - stats['unique']
    stats['time_first'] = videos[0]['watched']
    stats['time_last'] = videos[-1]['watched']

    return (videos, stats)
