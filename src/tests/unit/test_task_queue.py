# -*- coding: utf-8 -*-

"""Test module doc string."""
import json
from unittest.mock import patch

import pytest

from app import task_queue

"""
with patch('app.youtube._get_youtube') as mock_get_yt:
        mock_get_yt.side_effect = [resp_valid, resp_empty]
"""
def test_create_tasks(fix_task_list, fix_video_list):
    with patch('app.util.get_timestamp_utc') as mock_f:
        mock_f.return_value = '1970-01-01T00:00:00Z'

        result = task_queue.create_tasks(fix_video_list)
        assert fix_task_list == result


def test_load(tmp_path, fix_task_list):
    task_list = [x.copy() for x in fix_task_list[-3:]]
    task_list.extend([x.copy() for x in fix_task_list[-3:]])

    task_list[3].update({'state': 'ok', 'retry': 4})
    task_list[4].update({'state': 'failed', 'retry': 5})
    task_list[5].update({'state': 'error', 'retry': 4})

    queue_file = tmp_path / 'task.queue'

    with queue_file.open('w') as fd_out:
        for task in task_list:
            fd_out.write('{}\n'.format(json.dumps(task)))

    tasks = task_queue.load(queue_file)

    assert task_list[-1:] == tasks
