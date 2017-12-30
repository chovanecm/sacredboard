"""
Accessing the Metrics Data.

Issue: https://github.com/chovanecm/sacredboard/issues/58
"""
import datetime

from flask import Response, render_template, Blueprint, current_app

from sacredboard.app.data import NotFoundError

metrics = Blueprint("metrics", __name__)


def get_metric(run_id, metric_id):
    """
    Get a specific Sacred metric from the database.

    Returns a JSON response or HTTP 404 if not found.
    Issue: https://github.com/chovanecm/sacredboard/issues/58
    """
    data = current_app.config["data"]  # type: DataStorage
    dao = data.get_metrics_dao()
    metric = dao.get(run_id, metric_id)

    return Response(render_template(
        "api/metric.js",
        run_id=metric["run_id"],
        metric_id=metric["metric_id"],
        name=metric["name"],
        steps=metric["steps"],
        timestamps=metric["timestamps"],
        values=metric["values"]),
        mimetype="application/json")


@metrics.app_template_filter("format_metric_timestamp")
def format_metric_timestamp(timestamp: datetime.datetime):
    """
    Convert given timestamp to UTC string format.

    :param timestamp UTC time to convert.
    :type timestamp datetime.datetime

    :return str
    """
    return "%sZ" % timestamp.isoformat()


@metrics.route("/api/run/<int:run_id>/metric/<metric_id>")
def api_metric(run_id, metric_id):
    """
    Get Sacred metrics.

    Issue: https://github.com/chovanecm/sacredboard/issues/58
    The API will return an object of the metric with parameters

    {steps: [0,1,20,40,...],
    strtimesteps: [timestep1,timestep2,timestep3,...],
     values: [0,1 2,3,4,5,6,...],
     name: "name of the metric"}

    :param run_id: The ID of the run to search the metric for.
    :param metric_id: The metric ID.
    :return: JSON object in the given format.
    """
    return get_metric(run_id, metric_id)


@metrics.errorhandler(NotFoundError)
def handle_not_found_error(e):
    """Handle exception when a metric is not found."""
    return "Couldn't find resource:\n%s" % e, 404


def initialize(app, app_config):
    """Register the module in Flask."""
    app.register_blueprint(metrics)
