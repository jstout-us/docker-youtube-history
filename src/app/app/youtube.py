# -*- coding: utf-8 -*-

"""Module app.youtube."""
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from dateutil import parser
from dateutil import tz

MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
TIMEZONES = {
    'EDT': 'US/Eastern',
    'EST': 'US/Eastern'
    }


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


def parse_history(path):
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


        if data['vid_id']:
            videos.append(data)

    return videos
