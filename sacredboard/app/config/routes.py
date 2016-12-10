from flask import render_template
from flask import Blueprint
from flask import current_app
routes = Blueprint("routes", __name__)


@routes.route("/")
def hello_world():
    return "Hello world"


@routes.route("/runs")
def runs():
    data = current_app.config["data"]
    return render_template("runs.html", runs=data.runs(), type=type)


def setup_routes(app):
    app.register_blueprint(routes)
