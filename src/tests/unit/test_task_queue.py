# -*- coding: utf-8 -*-

"""Test module doc string."""
import json

from app import task_queue


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

    # print(task_list)
    # print('\n=============================\n')
    # print(tasks)

    assert task_list[-1:] == tasks
    # assert True == False
