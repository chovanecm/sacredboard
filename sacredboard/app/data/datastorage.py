"""Interfaces for data storage."""
from sacredboard.app.data.rundao import RunDAO
from .errors import NotFoundError
from .filesdao import FilesDAO
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

    def get_metrics_dao(self) -> MetricsDAO:
        """
        Return a data access object for metrics.

        By default, returns a dummy Data Access Object if not overridden.
        Issue: https://github.com/chovanecm/sacredboard/issues/62

        :return MetricsDAO
        """
        return DummyMetricsDAO()

    def get_run_dao(self) -> RunDAO:
        """
        Return a data access object for Runs.

        :return: RunDAO
        """
        raise NotImplementedError(
            "Run Data Access Object must be implemented.")

    def get_files_dao(self) -> FilesDAO:
        """
        Return a data access object for files.

        :return: FilesDAO
        """
        raise NotImplementedError(
            "Artifacts Data Access Object must be implemented.")


class DummyMetricsDAO(MetricsDAO):
    """Dummy Metrics DAO that does not find any metric."""

    def get(self, run_id, metric_id):
        """
        Raise NotFoundError. Always.

        :raise NotFoundError
        """
        raise NotFoundError("Metrics not supported by this backend.")

    def delete(self, run_id):
        """Do nothing."""
        pass
