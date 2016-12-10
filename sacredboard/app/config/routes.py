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
    draw = (int)(request.args.get("draw"))
    data = current_app.config["data"]
    runs = data.runs()
    records_total = runs.count()
    records_filtered = runs.count()
    return Response(render_template("api/runs.js", runs=runs, draw=draw, recordsTotal=records_total,
                                    recordsFiltered=records_filtered), mimetype="application/json")


def setup_routes(app):
    app.register_blueprint(routes)
