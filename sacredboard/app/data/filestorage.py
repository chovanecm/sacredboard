import datetime
import os
import json

from sacredboard.app.data.datastorage import Cursor, DataStorage

config_json = "config.json"
run_json = "run.json"


def _path_to_config(basepath, run_id):
    return os.path.join(basepath, str(run_id), config_json)


def _path_to_run(basepath, run_id):
    return os.path.join(basepath, str(run_id), run_json)


def _read_json(path_to_json):
    with open(path_to_json) as f:
        return json.load(f)


def _create_run(runjson, configjson):
    runjson["config"] = configjson

    # TODO probably want a smarter way of detecting
    # which values have type "time."
    for k in ["start_time", "stop_time", "heartbeat"]:
        runjson[k] = datetime.datetime.strptime(runjson[k],
                                                '%Y-%m-%dT%H:%M:%S.%f')
    return runjson


class FileStoreCursor(Cursor):
    def __init__(self, count, iterable):
        self.iterable = iterable
        self._count = count

    def count(self):
        return self._count

    def __iter__(self):
        return iter(self.iterable)


class FileStorage(DataStorage):
    def __init__(self, path_to_dir):
        super().__init__()
        self.path_to_dir = os.path.expanduser(path_to_dir)

    def get_run(self, run_id):
        config = _read_json(_path_to_config(self.path_to_dir, run_id))
        run = _read_json(_path_to_run(self.path_to_dir, run_id))
        return _create_run(run, config)

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):

        all_run_ids = os.listdir(self.path_to_dir)

        def run_iterator():
            blacklist = set(["_sources"])
            for id in all_run_ids:
                if id in blacklist:
                    continue

                yield self.get_run(id)

        count = len(all_run_ids)
        return FileStoreCursor(count, run_iterator())
