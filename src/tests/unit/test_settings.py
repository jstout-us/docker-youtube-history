# -*- coding: utf-8 -*-

"""Test module doc string."""
from datetime import datetime

import pytest

from app import settings


def test_timestamp_iso_format():
    expected = '1970-01-02T01:02:03Z'
    result = datetime(1970, 1, 2, 1, 2, 3).strftime(settings.TIMESTAMP_ISO_FORMAT)

    assert expected == result


def test_get_file_timestamp():
    expected = '19700102_010203'
    result = datetime(1970, 1, 2, 1, 2, 3).strftime(settings.TIMESTAMP_FILE_FORMAT)

    assert expected == result
