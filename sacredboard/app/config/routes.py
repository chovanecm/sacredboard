import re

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request, Response, redirect

import sacredboard.app.process.process as proc

routes = Blueprint("routes", __name__)


@routes.route("/")
def hello_world():
    return "Hello world"


@routes.route("/runs")
def runs():
    data = current_app.config["data"]
    # return render_template("runs.html", runs=data.runs(), type=type)
    return render_template("runs.html", runs=[], type=type)


@routes.route("/api/run")
def api_runs():
    data = current_app.config["data"]
    # TODO: Move the logic somewhere else?
    draw = request.args.get("draw")
    draw = (int)(draw) if draw is not None else 1
    start = 0 if not request.args.get("start") else (int)(request.args.get("start"))
    length = -1 if not request.args.get("length") else (int)(request.args.get("length"))
    length = length if length >= 0 else None

    # TODO: Make it work with heartbeat_diff
    order_column = request.args.get("order[0][column]")
    order_dir = request.args.get("order[0][dir]")
    if order_column is not None:
        order_column = request.args.get("columns[%d][name]" % (int)(order_column))
        if order_column == "hostname":
            order_column = "host.hostname"
    runs = data.get_runs(start=start, limit=length, sort_by=order_column, sort_direction=order_dir)
    # records_total should be the total size of the records in the databse, not fo that what was returned
    records_total = runs.count()
    records_filtered = runs.count()
    return Response(render_template("api/runs.js", runs=runs, draw=draw, recordsTotal=records_total,
                                    recordsFiltered=records_filtered), mimetype="application/json")


@routes.route("/api/run/<run_id>")
def api_run(run_id):
    data = current_app.config["data"]
    run = data.get_run(run_id)
    records_total = 1 if run is not None else 0
    records_filtered = records_total
    return Response(render_template("api/runs.js", runs=[run], draw=1, recordsTotal=records_total,
                                    recordsFiltered=records_filtered, full_object=True), mimetype="application/json")


@routes.route("/tensorboard/<run_id>/<int:tflog_id>")
def run_tensorboard(run_id, tflog_id):
    data = current_app.config["data"]
    # optimisticaly suppose the run exists...
    run = data.get_run(run_id);
    base_dir = run["experiment"]["base_dir"];
    log_dir = run["info"]["tensorflow"]["logdirs"][tflog_id]
    # TODO ugly!!!
    path_to_log_dir = base_dir + "/" + log_dir
    port = int(proc.run_tensorboard(path_to_log_dir))
    url_root = request.url_root
    url_parts = re.search("://([^:/]+)", url_root)
    redirect_to_address = url_parts.group(1)
    return redirect("http://%s:%d" % (redirect_to_address, port))



def setup_routes(app):
    app.register_blueprint(routes)
