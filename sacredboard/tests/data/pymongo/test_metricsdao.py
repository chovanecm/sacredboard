import datetime

import mongomock
import pytest
from bson import ObjectId

from sacredboard.app.data import NotFoundError
from sacredboard.app.data.pymongo.genericdao import GenericDAO
from sacredboard.app.data.pymongo.metricsdao import MongoMetricsDAO
from sacredboard.tests.fixtures.metrics import m1, m2, m3


def mongo_client():
    client = mongomock.MongoClient()
    db = client.testdb
    db.metrics.insert_one(m1)
    db.metrics.insert_one(m2)
    db.metrics.insert_one(m3)
    return client


def generic_dao():
    client = mongo_client()
    return GenericDAO(client, "testdb")


@pytest.fixture
def metrics_dao():
    dao = generic_dao()
    return MongoMetricsDAO(dao)


def test_get_metric(metrics_dao: MongoMetricsDAO):
    metric = metrics_dao.get(14, "58dcfc41263e8cc29ade7a26")
    assert type(metric) == dict
    assert metric["run_id"] == 14
    assert metric["metric_id"] == "58dcfc41263e8cc29ade7a26"
    assert type(metric["timestamps"][0]) == datetime.datetime


def test_get_metric_that_does_not_exist(metrics_dao: MongoMetricsDAO):
    with pytest.raises(NotFoundError):
        metric = metrics_dao.get(14, "DOES_NOT_EXIST")
        pytest.fail("Given metric does not exist. NotFoundError should"
                    " have been raised!")


def test_delete_one_metric(metrics_dao: MongoMetricsDAO):
    # Test that the metric exists:
    metric = metrics_dao.get(15, "58dcfc41263e8cc29ade7a27")
    assert type(metric) == dict \
           and metric["metric_id"] == "58dcfc41263e8cc29ade7a27", \
        "The test configuration is invalid."
    # Delete metric
    metrics_dao.delete(run_id=15)
    with pytest.raises(NotFoundError):
        metric = metrics_dao.get(15, "58dcfc41263e8cc29ade7a27")


def test_delete_many_metrics(metrics_dao: MongoMetricsDAO):
    # Test that the metrics exist:
    metric = metrics_dao.get(14, "58dcfc41263e8cc29ade7a25")
    assert type(metric) == dict \
           and metric["metric_id"] == "58dcfc41263e8cc29ade7a25", \
        "The test configuration is invalid."

    metric = metrics_dao.get(14, "58dcfc41263e8cc29ade7a26")
    assert type(metric) == dict \
           and metric["metric_id"] == "58dcfc41263e8cc29ade7a26", \
        "The test configuration is invalid."

    # Delete metric
    metrics_dao.delete(run_id=14)

    with pytest.raises(NotFoundError):
        metric = metrics_dao.get(14, "58dcfc41263e8cc29ade7a25")

    with pytest.raises(NotFoundError):
        metric = metrics_dao.get(14, "58dcfc41263e8cc29ade7a26")

