"""Interfaces for data storage backend."""

class Cursor:
    """Interface that abstracts the cursor object returned from databases."""

    def __init__(self):
        pass

    def count(self):
        """Return the number of items in this cursor."""
        raise NotImplemented()

    def __iter__(self):
        raise NotImplemented()


class DataStorage:
    """
    Interface for data backends. Defines the API for various data stores --- databases, file stores, etc. --- that
    sacred supports.
    """

    def __init__(self):
        pass

    def get_run(self, run_id):
        """Return the run associated with the id."""
        raise NotImplemented()

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):
        """Return all runs that match the query."""
        raise NotImplemented()
