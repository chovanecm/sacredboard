"""Errors that might occur during data access."""


class NotFoundError(Exception):
    """Record not found exception."""

    def __init__(self, *args, **kwargs):
        """Record not found exception."""
        Exception.__init__(self, *args, **kwargs)


class DataSourceError(Exception):
    """Error when accessing the data source."""

    def __init__(self, *args, **kwargs):
        """Error when accessing the data source."""
        Exception.__init__(self, *args, **kwargs)
