from flask import render_template
from flask import Blueprint
from flask import current_app
from flask import request, Response

routes = Blueprint("routes", __name__)


@routes.route("/")
def hello_world():
    return "Hello world"


@routes.route("/runs")
def runs():
    data = current_app.config["data"]
    # return render_template("runs.html", runs=data.runs(), type=type)
    return render_template("runs.html", runs=[], type=type)


@routes.route("/api/runs")
def api_runs():

    data = current_app.config["data"]
    # TODO: Move the logic somewhere else?
    draw = (int)(request.args.get("draw"))

    start = 0 if not request.args.get("start") else (int)(request.args.get("start"))
    length = -1 if not request.args.get("length") else (int)(request.args.get("length"))
    length = length if length >= 0 else None

    # TODO: Make it work with heartbeat_diff
    order_column = request.args.get("order[0][column]")
    order_dir = request.args.get("order[0][dir]")
    if order_column is not None:
        order_column = request.args.get("columns[%d][name]" % (int)(order_column))
    runs = data.runs(start=start, limit=length, sort_by=order_column, sort_direction=order_dir)

    # records_total should be the total size of the records in the databse, not fo that what was returned
    records_total = runs.count()
    records_filtered = runs.count()
    return Response(render_template("api/runs.js", runs=runs, draw=draw, recordsTotal=records_total,
                                    recordsFiltered=records_filtered), mimetype="application/json")


def setup_routes(app):
    app.register_blueprint(routes)
