"""
Implementation of cursor for iterating over results.

Backed by pymongo cursor.
"""
from sacredboard.app.data.datastorage import Cursor


class MongoDbCursor(Cursor):
    """Implements Cursor for mongodb."""

    def __init__(self, mongodb_cursor):
        """Initialize a MongoDB cursor."""
        self.mongodb_cursor = mongodb_cursor

    def count(self):
        """Return the number of items in this cursor."""
        return self.mongodb_cursor.count()

    def __iter__(self):
        """Iterate over runs."""
        return self.mongodb_cursor
