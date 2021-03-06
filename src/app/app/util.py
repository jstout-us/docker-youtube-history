# -*- coding: utf-8 -*-

"""Module app.util."""
import json
import pickle
import time
from datetime import datetime
from datetime import timedelta

from . import settings


def _load_json(path):
    with path.open() as fd_in:
        data = json.load(fd_in)

    return data


def _load_pickle(path):
    with path.open('rb') as fd_in:
        data = pickle.load(fd_in)

    return data


def _save_json(path, data):
    with path.open('w') as fd_out:
        json.dump(data, fd_out, indent=4, sort_keys=True)


def _save_pickle(path, data):
    with path.open('wb') as fd_out:
        pickle.dump(data, fd_out)


EXTENSIONS = {
    '.json': {
        'r': _load_json,
        'w': _save_json
        },
    '.pkl': {
        'r': _load_pickle,
        'w': _save_pickle
        }
    }


def get_file_timestamp():
    """Return formated file name utc timestamp.

    Returns
        timestamp(str)
    """
    return datetime.utcnow().strftime(settings.TIMESTAMP_FILE_FORMAT)


def get_sleep_time(time_start, time_now, poll_int):
    """Calculate time to sleep.

    Args:
        time_start(datetime):   Time loop started
        time_now(datetime):     Current time
        poll_int(int):          Poll interval in seconds

    Returns:
        sleep_time(float)
    """
    time_sleep = poll_int - (time_now - time_start).total_seconds()

    if time_sleep < 0:
        time_sleep = 0

    return time_sleep


def get_timestamp_utc():
    """Return formated ISO formated UTC timestamp.

    Returns
        timestamp(str)
    """
    return datetime.utcnow().strftime(settings.TIMESTAMP_ISO_FORMAT)


def get_time_remaining(task_cnt, poll_int):
    """Calculate time remaining.

    Args:
        task_cnt(int):  Total task remaining
        poll_int(int):  API Poll interval

    Returns:
        str:            Formated time remaining
    """
    delta = timedelta(seconds=task_cnt*poll_int)

    days_str = ''
    if delta.days > 1:
        days_str = '{} days, '.format(delta.days)

    elif delta.days == 1:
        days_str = '{} day, '.format(delta.days)

    time_str = time.strftime('%H:%M', time.gmtime(delta.seconds))
    # time_str = time.gmtime(delta.seconds).strftime('%H:%M')

    return ''.join([days_str, time_str])


def load_file(path):
    """Deseralize and return file contents.

    Args:
        path(Path): Path to file

    Returns:
        file contents
    """
    return EXTENSIONS[path.suffix]['r'](path)


def save_file(path, data):
    """Serialize data and write to disk.

    Args:
        path(Path): Path to output file
        data(*):    Any serializable object

    Returns:
        None
    """
    return EXTENSIONS[path.suffix]['w'](path, data)
