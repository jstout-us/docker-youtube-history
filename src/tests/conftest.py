import pytest

@pytest.fixture
def fix_task_list():
    fixture = [
        {
            'id': 'c_1',
            'kind': 'channel',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        {
            'id': 'c_2',
            'kind': 'channel',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        {
            'id': 'v_1',
            'kind': 'video',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        {
            'id': 'v_2',
            'kind': 'video',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        {
            'id': 'v_3',
            'kind': 'video',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        {
            'id': 'v_4',
            'kind': 'video',
            'state': 'queued',
            'retry': 5,
            'timestamp': '1970-01-01T00:00:00Z'
            },
        ]

    return fixture
