from sacredboard.app.data import DataStorage


class RunFacade:
    def __init__(self, datastorage: DataStorage):
        self.datastorage = datastorage

    def delete_run(self, run_id):
        ds = self.datastorage
        ds.get_metrics_dao().delete(run_id)
        ds.get_artifact_dao().delete(run_id)
        ds.get_resource_dao().delete(run_id)
        ds.get_run_dao().delete(run_id)
