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


@pytest.fixture
def fix_video_list():
    fixture = [
        {
            'chan_id': 'c_1',
            'chan_title': 'Channel 1',
            'vid_id': 'v_1',
            'vid_title': 'Video 1',
            'watched': '1970-01-01T12:00:00Z'
            },
        {
            'chan_id': 'c_1',
            'chan_title': 'Channel 1',
            'vid_id': 'v_2',
            'vid_title': 'Video 2',
            'watched': '1970-02-01T12:00:00Z'
            },
        {
            'chan_id': 'c_2',
            'chan_title': 'Channel 2',
            'vid_id': 'v_3',
            'vid_title': 'Video 3',
            'watched': '1970-03-01T12:00:00Z'
            },
        {
            'chan_id': None,
            'chan_title': None,
            'vid_id': 'v_4',
            'vid_title': 'Video 4',
            'watched': '1970-04-01T12:00:00Z'
            },
        {
            'chan_id': 'c_1',
            'chan_title': 'Channel 1',
            'vid_id': 'v_1',
            'vid_title': 'Video 1',
            'watched': '1970-05-01T12:00:00Z'
            },
        ]

    return fixture
