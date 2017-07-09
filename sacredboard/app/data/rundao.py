"""
Interface for accessing Sacred metrics.

Issue: https://github.com/chovanecm/sacredboard/issues/69
"""


class RunDAO:
    """
    Interface for accessing Runs.

    Issue: https://github.com/chovanecm/sacredboard/issues/69
    """

    def get_run(self, run_id):
        """Return the run associated with the id."""
        raise NotImplementedError("RunDAO is abstract.")

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):
        """Return all runs that match the query."""
        raise NotImplementedError("RunDAO is abstract.")

    def delete_run(self, run_id, run_only=False):
        """
        Delete run with the given id from the backend.

        :param run_id: Id of the run to delete.
        :param run_only: If true, only the run object is deleted. If false, the
        backend may delete additional related records as well.
        :type bool
        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found. (Some backends may succeed
        even if the run does not exist.
        """
        raise NotImplementedError(
            "This database data source does not currently support this "
            "operation.")
