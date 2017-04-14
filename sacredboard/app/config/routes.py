# coding=utf-8
import re
from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request, Response, redirect, url_for
from pathlib import Path

import sacredboard.app.process.process as proc
import sacredboard.app.process.tensorboard
from sacredboard.app.controller.runs import get_runs
from ..process import process

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    return redirect(url_for("routes.show_runs"))


@routes.route("/_tests")
def tests():
    return redirect(url_for("static", filename="tests/index.html"))

@routes.route("/runs")
def show_runs():
    # return render_template("runs.html", runs=data.runs(), type=type)
    return render_template("runs.html", runs=[], type=type)


@routes.route("/api/run")
def api_runs():
    return get_runs()


@routes.route("/api/run/<run_id>")
def api_run(run_id):
    data = current_app.config["data"]
    run = data.get_run(run_id)
    records_total = 1 if run is not None else 0
    records_filtered = records_total
    return Response(render_template("api/runs.js", runs=[run], draw=1,
                                    recordsTotal=records_total,
                                    recordsFiltered=records_filtered,
                                    full_object=True),
                    mimetype="application/json")


@routes.route("/tensorboard/start/<run_id>/<int:tflog_id>")
def run_tensorboard(run_id, tflog_id):
    data = current_app.config["data"]
    # optimisticaly suppose the run exists...
    run = data.get_run(run_id)
    base_dir = Path(run["experiment"]["base_dir"])
    log_dir = Path(run["info"]["tensorflow"]["logdirs"][tflog_id])
    # TODO ugly!!!
    if log_dir.is_absolute():
        path_to_log_dir = log_dir
    else:
        path_to_log_dir = base_dir.joinpath(log_dir)

    port = int(sacredboard.app.process.tensorboard.run_tensorboard(str(path_to_log_dir)))
    url_root = request.url_root
    url_parts = re.search("://([^:/]+)", url_root)
    redirect_to_address = url_parts.group(1)
    return redirect("http://%s:%d" % (redirect_to_address, port))


@routes.route("/tensorboard/stop")
def close_tensorboards():
    sacredboard.app.process.tensorboard.stop_all_tensorboards()
    return "Stopping tensorboard"


@routes.errorhandler(sacredboard.app.process.tensorboard.TensorboardNotFoundError)
def handle_tensorboard_not_found(e):
    return "Tensorboard not found on your system." \
           " Please install tensorflow first. Sorry.", 503


@routes.errorhandler(TimeoutError)
def handle_tensorboard_timeout(e):
    return "Tensorboard does not respond. Sorry.", 503


@routes.errorhandler(process.UnexpectedOutputError)
def handle_tensorboard_unexpected_output(e: process.UnexpectedOutputError):
    return "Tensorboard outputted '%s'," \
           " but the information expected was: '%s'. Sorry."\
           % (e.output, e.expected), 503


def setup_routes(app):
    app.register_blueprint(routes)
