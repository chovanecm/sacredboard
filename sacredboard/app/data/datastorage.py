class Cursor:
    def __init__(self):
        pass

    def count(self):
        raise NotImplemented()

    def __iter__(self):
        raise NotImplemented()


class DataStorage:
    def __init__(self):
        pass

    def get_run(self, run_id):
        raise NotImplemented()

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):
        raise NotImplemented()
