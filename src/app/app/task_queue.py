# -*- coding: utf-8 -*-

"""Module app.task_queue."""
import json

def create(videos):
    return []


def load(path):
    tasks = {}
    with path.open() as fd_in:
        for line in fd_in:
            task = json.loads(line)
            tasks[task['id']] = task

    return [x for x in tasks.values() if x['state'] not in ('failed', 'ok')]


def save(path, *args):
    pass
