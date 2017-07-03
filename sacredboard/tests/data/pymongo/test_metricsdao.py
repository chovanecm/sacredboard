import datetime

import mongomock
import pytest
from bson import ObjectId

from sacredboard.app.data.pymongo.genericdao import GenericDAO
from sacredboard.app.data.pymongo.metricsdao import MongoMetricsDAO


def mongo_client():
    client = mongomock.MongoClient()
    db = client.testdb
    m1 = {'_id': ObjectId('58dcfc41263e8cc29ade7a25'),
          'name': 'training.accuracy',
          'run_id': 14,
          'timestamps': [datetime.datetime(2017, 3, 30, 12, 38, 18, 424000),
                         datetime.datetime(2017, 3, 30, 12, 38, 33, 732000),
                         datetime.datetime(2017, 3, 30, 12, 38, 49, 470000),
                         datetime.datetime(2017, 3, 30, 12, 39, 4, 694000),
                         datetime.datetime(2017, 3, 30, 12, 39, 19, 912000),
                         datetime.datetime(2017, 3, 30, 12, 39, 36, 857000)],
          'steps': [0, 5, 10, 15, 20, 25],
          'values': [0.2139461189508438,
                     0.5467512011528015,
                     0.6640253663063049,
                     0.6798732280731201,
                     0.7527734041213989,
                     0.7670364379882812]}
    m2 = {'_id': ObjectId('58dcfc41263e8cc29ade7a26'),
          'name': 'validation.cost',
          'run_id': 14,
          'timestamps': [datetime.datetime(2017, 3, 30, 12, 38, 18, 424000),
                         datetime.datetime(2017, 3, 30, 12, 38, 33, 732000),
                         datetime.datetime(2017, 3, 30, 12, 38, 49, 471000),
                         datetime.datetime(2017, 3, 30, 12, 39, 4, 694000),
                         datetime.datetime(2017, 3, 30, 12, 39, 19, 912000),
                         datetime.datetime(2017, 3, 30, 12, 39, 36, 857000)],
          'steps': [0, 5, 10, 15, 20, 25],
          'values': [542.752685546875,
                     527.7616577148438,
                     563.5029296875,
                     617.9539794921875,
                     690.0741577148438,
                     788.0784301757812]}
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
