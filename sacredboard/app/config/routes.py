from flask import render_template
from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/")
def hello_world():
    return "Hello world"


@routes.route("/runs")
def runs():
    return render_template("runs.html", runs=routes.sacred_data.runs(), type=type)


def setup_routes(app):
    app.register_blueprint(routes)
    routes.sacred_data = app.config["data"]
