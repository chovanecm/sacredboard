"""
Module responsible for accessing the Metrics data in MongoDB.

Issue: https://github.com/chovanecm/sacredboard/issues/60
"""

from bson import ObjectId
from bson.errors import InvalidId

from sacredboard.app.data import NotFoundError
from .genericdao import GenericDAO
from ..metricsdao import MetricsDAO


class MongoMetricsDAO(MetricsDAO):
    """Implementation of MetricsDAO for MongoDB."""

    def __init__(self, generic_dao: GenericDAO):
        """
        Create new metrics accessor for MongoDB.

        :param generic_dao: A configured generic MongoDB data access object
         pointing to an appropriate database.
        """
        self.generic_dao = generic_dao
        self.metrics_collection_name = "metrics"
        """Name of the MongoDB collection with metrics."""

    def get_metric(self, run_id, metric_id):
        """
        Read a metric of the given id and run.

        The returned object has the following format (timestamps are datetime
         objects).

        .. code::

            {"steps": [0,1,20,40,...],
            "timestamps": [timestamp1,timestamp2,timestamp3,...],
            "values": [0,1 2,3,4,5,6,...],
            "name": "name of the metric",
            "metric_id": "metric_id",
            "run_id": "run_id"}

        :param run_id: ID of the Run that the metric belongs to.
        :param metric_id: The ID fo the metric.
        :return: The whole metric as specified.

        :raise NotFoundError
        """
        query = self._build_query(run_id, metric_id)
        row = self._read_metric_from_db(metric_id, run_id, query)
        metric = self._to_intermediary_object(row)
        return metric

    def _read_metric_from_db(self, metric_id, run_id, query):
        row = self.generic_dao.find_record(self.metrics_collection_name, query)
        if row is None:
            raise NotFoundError("Metric %s for run %s not found."
                                % (metric_id, run_id))
        return row

    def _build_query(self, run_id, metric_id):
        # Metrics in MongoDB is always an ObjectId
        try:
            id = ObjectId(metric_id)
            return {"run_id": run_id, "_id": id}
        except InvalidId as ex:
            raise NotFoundError("Metric Id %s is invalid "
                                "ObjectId in MongoDB" % metric_id) from ex

    def _to_intermediary_object(self, row):
        return {
            "metric_id": str(row["_id"]),
            "run_id": row["run_id"],
            "name": row["name"],
            "steps": row["steps"],
            "timestamps": row["timestamps"]
        }
