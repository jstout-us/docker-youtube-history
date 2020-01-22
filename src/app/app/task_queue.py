# -*- coding: utf-8 -*-

"""Module app.task_queue."""
import itertools
import json
from collections import OrderedDict

from app import settings
from app import util


TEMPLATE_TASK = {
    'state': 'queued',
    'retry': 5,
    }


def create_tasks(videos):
    chan_ = OrderedDict()
    vid_ = OrderedDict()

    for video in videos:
        chan_[video['chan_id']] = 'channel'
        vid_[video['vid_id']] = 'video'

    chan_.pop(None)
    tasks = []

    for key, value in itertools.chain(chan_.items(), vid_.items()):
        task = TEMPLATE_TASK.copy()
        task['id'] = key
        task['kind'] = value
        task['timestamp'] = util.get_timestamp_utc()

        tasks.append(task)

    return tasks


def load(path):
    tasks = {}
    with path.open() as fd_in:
        for line in fd_in:
            task = json.loads(line)
            tasks[task['id']] = task

    return [x for x in tasks.values() if x['state'] not in ('failed', 'ok')]


def save(path, *args):
    pass
