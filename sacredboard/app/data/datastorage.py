"""Interfaces for data storage."""
from .errors import NotFoundError, DataSourceError
from .metricsdao import MetricsDAO


class Cursor:
    """Interface that abstracts the cursor object returned from databases."""

    def __init__(self):
        """Declare a new cursor to iterate over runs."""
        pass

    def count(self):
        """Return the number of items in this cursor."""
        raise NotImplementedError()

    def __iter__(self):
        """Iterate over elements."""
        raise NotImplementedError()


class DataStorage:
    """
    Interface for data backends.

    Defines the API for various data stores
    databases, file stores, etc. --- that sacred supports.
    """

    def __init__(self):
        """Initialize data accessor."""
        pass

    def get_run(self, run_id):
        """Return the run associated with the id."""
        raise NotImplementedError()

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):
        """Return all runs that match the query."""
        raise NotImplementedError()

    def delete_run(self, run_id, run_only=False):
        """
        Delete run with the given id from the backend.

        :param run_id: Id of the run to delete.
        :param run_only: If true, only the run object is deleted. If false, the
        backend may delete additional related records as well.
        :type bool
        :raise NotImplementedError If not supported by the backend.
        """
        raise DataSourceError("This database data source does not currently "
                              "support this operation.")

    def get_metrics_dao(self):
        """
        Return a data access object for metrics.

        By default, returns a dummy Data Access Object if not overridden.
        Issue: https://github.com/chovanecm/sacredboard/issues/62

        :return MetricsDAO
        """
        return DummyMetricsDAO()


class DummyMetricsDAO(MetricsDAO):
    """Dummy Metrics DAO that does not find any metric."""

    def get_metric(self, run_id, metric_id):
        """
        Raise NotFoundError. Always.

        :raise NotFoundError
        """
        raise NotFoundError("Metrics not supported by this backend.")
