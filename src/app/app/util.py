# -*- coding: utf-8 -*-

"""Module app.util."""
import pickle
from datetime import datetime

from . import settings


def get_timestamp_utc():
    return datetime.utcnow().strftime(settings.TIMESTAMP_ISO_FORMAT)


def load_file(path):
    """Deseralize and return file contents.

    Args:
        path(Path): Path to file

    Returns:
        file contents
    """
    with path.open('rb') as fd_in:
        data = pickle.load(fd_in)

    return data
