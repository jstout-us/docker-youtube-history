# -*- coding: utf-8 -*-

"""Module app.util."""
import pickle

def load_file(path):
    with path.open('rb') as fd_in:
        data = pickle.load(fd_in)

    return data
