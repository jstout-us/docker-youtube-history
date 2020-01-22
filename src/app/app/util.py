# -*- coding: utf-8 -*-

"""Module app.util."""
import pickle


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
