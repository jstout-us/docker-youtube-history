# -*- coding: utf-8 -*-

"""Module app.task_queue."""
import itertools
import json
from collections import OrderedDict

from app import util


TEMPLATE_TASK = {
    'state': 'queued',
    'retry': 5,
    }


def create_tasks(videos):
    """Create a list of task objects from list of video objects.

    Args:
        videos(list):   List of video dictionaries

    Returns;
        tasks(list):    List of task dictionaries.
    """
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
    """Load tasks from task queue file.

    Args:
        path(Path): path to task.queue file

    Returns:
        tasks(list): list of active task dictionaries
    """
    tasks = {}
    with path.open() as fd_in:
        for line in fd_in:
            task = json.loads(line)
            tasks[task['id']] = task

    return [x for x in tasks.values() if x['state'] not in ('failed', 'ok')]


def save(path, *tasks):
    """Save task dictionaries to disk.

    Args:
        path(Path):     path to task.queue file
        tasks(dict):    One or more task dictionaries

    Returns:
        None
    """
    with path.open('a') as fd_out:
        for task in tasks:
            task_ = task.copy()
            task_['timestamp'] = util.get_timestamp_utc()
            fd_out.write('{}\n'.format(json.dumps(task_)))
