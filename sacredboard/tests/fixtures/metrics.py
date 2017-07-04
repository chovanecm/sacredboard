"""Metrics for test purposes (mainly for the PyMongo backend)."""
import datetime

from bson import ObjectId

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
