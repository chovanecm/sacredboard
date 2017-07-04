import pytest
import simplejson
from flask import Flask

from sacredboard import bootstrap
from sacredboard.app.data import MetricsDAO, NotFoundError, DataStorage
from sacredboard.app.webapi import metrics
from sacredboard.tests.fixtures.metrics import m1, m2

app = None
test_client = None


class FakeMetricsDAO(MetricsDAO):
    def get_metric(self, run_id, metric_id):
        if metric_id == "58dcfc41263e8cc29ade7a25":
            row = m1
        elif metric_id == "58dcfc41263e8cc29ade7a26":
            row = m2
        else:
            raise NotFoundError("Metric %s not found" % metric_id)
        return {
            "metric_id": str(row["_id"]),
            "run_id": row["run_id"],
            "name": row["name"],
            "steps": row["steps"],
            "timestamps": row["timestamps"],
            "values": row["values"]
        }


class FakeDataStorage(DataStorage):
    def get_metrics_dao(self):
        return FakeMetricsDAO()


@pytest.fixture(scope="session", autouse=True)
def init_tests():
    global app
    global test_client
    app = bootstrap.app
    app.testing = True
    app.config["data"] = FakeDataStorage()
    test_client = app.test_client()
    metrics.initialize(app)


def test_get_metric():
    response = test_client.get("/api/run/0/metric/58dcfc41263e8cc29ade7a25")
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    metric_json = response.data
    metric = simplejson.loads(metric_json)
    expected_keys = ["steps", "strtimestamps", "values", "name", "metric_id",
                     "run_id"]
    for expected_key in expected_keys:
        assert expected_key in metric, "Key %s was not found in the returned object, but it's mandatory!" % expected_key
        assert metric[expected_key] is not None

    expected_array_keys = ["steps", "strtimestamps", "values"]
    for expected_array_key in expected_array_keys:
        assert type(metric[
                        expected_array_key]) == list, "%s should be a list." % expected_array_key

    assert metric["name"] == "training.accuracy"
    assert metric["run_id"] == 14
    assert metric["metric_id"] == "58dcfc41263e8cc29ade7a25"
    assert metric["values"] == [0.2139461189508438, 0.5467512011528015,
                                0.6640253663063049, 0.6798732280731201,
                                0.7527734041213989, 0.7670364379882812]
    assert len(metric["strtimestamps"]) == 6
    assert metric["strtimestamps"][2] == "2017-03-30T12:38:49.470000Z"


def test_get_metric_not_found():
    response = test_client.get("/api/run/0/metric/BLABLA")
    assert response.status_code == 404
