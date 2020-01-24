# -*- coding: utf-8 -*-

"""Module app.settings."""

LOG_FILE_MSG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
LOG_FILE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

LOG_STREAM_MSG_FORMAT = '%(asctime)s:%(levelname)s - %(message)s'
LOG_STREAM_TIME_FORMAT = '%H:%M:%S'

TIMESTAMP_FILE_FORMAT = '%Y%m%d_%H%M%S'
TIMESTAMP_ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

config = {}     # pylint: disable=invalid-name
