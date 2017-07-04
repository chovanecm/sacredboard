import datetime

import mongomock
import pytest
from bson import ObjectId

from sacredboard.app.data import NotFoundError
from sacredboard.app.data.pymongo.genericdao import GenericDAO
from sacredboard.app.data.pymongo.metricsdao import MongoMetricsDAO
from sacredboard.tests.fixtures.metrics import m1, m2


def mongo_client():
    client = mongomock.MongoClient()
    db = client.testdb
    db.metrics.insert_one(m1)
    db.metrics.insert_one(m2)
    return client


def generic_dao():
    client = mongo_client()
    return GenericDAO(client, "testdb")


@pytest.fixture
def metrics_dao():
    dao = generic_dao()
    return MongoMetricsDAO(dao)


def test_get_metric(metrics_dao: MongoMetricsDAO):
    metric = metrics_dao.get_metric(14, "58dcfc41263e8cc29ade7a26")
    assert type(metric) == dict
    assert metric["run_id"] == 14
    assert metric["metric_id"] == "58dcfc41263e8cc29ade7a26"
    assert type(metric["timestamps"][0]) == datetime.datetime


def test_get_metric_that_does_not_exist(metrics_dao: MongoMetricsDAO):
    with pytest.raises(NotFoundError):
        metric = metrics_dao.get_metric(14, "DOES_NOT_EXIST")
        pytest.fail("Given metric does not exist. NotFoundError should"
                    " have been raised!")
