"""
Interface for accessing Sacred metrics.

Issue: https://github.com/chovanecm/sacredboard/issues/60
"""


class MetricsDAO:
    """
    Interface for accessing Sacred metrics.

    Issue: https://github.com/chovanecm/sacredboard/issues/58
    """

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
        raise NotImplementedError("The MetricsDAO method is abstract.")
