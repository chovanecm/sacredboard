"""Enables a more complex manipulation with Runs."""
from sacredboard.app.data import DataStorage


class RunFacade:
    """Enables a more complex manipulation with Runs."""

    def __init__(self, datastorage: DataStorage):
        self.datastorage = datastorage

    def delete_run(self, run_id):
        """
        Delete run of the given run_id.

        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found. (Some backends may succeed even if the run does not exist.
        """
        ds = self.datastorage
        ds.get_metrics_dao().delete(run_id)
        # TODO: implement
        # ds.get_artifact_dao().delete(run_id)
        # ds.get_resource_dao().delete(run_id)
        ds.get_run_dao().delete(run_id)
