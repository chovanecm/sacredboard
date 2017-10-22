"""Implements Cursor for file storage."""
from sacredboard.app.data import Cursor


class FileStoreCursor(Cursor):
    """Implements Cursor for file storage."""

    def __init__(self, count, iterable):
        """Initialize FileStoreCursor with a given iterable."""
        self.iterable = iterable
        self._count = count

    def count(self):
        """
        Return the number of runs in this query.

        :return: int
        """
        return self._count

    def __iter__(self):
        """Iterate over runs."""
        return iter(self.iterable)
