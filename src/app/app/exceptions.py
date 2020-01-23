# -*- coding: utf-8 -*-

"""Module app.exceptions."""


class EmptyResponseError(Exception):
    """Exception raised for empty youtube response."""


class NotAuthenticatedError(Exception):
    """Exception raised for deleted videos."""
