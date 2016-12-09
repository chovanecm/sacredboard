from flask import render_template


def setup_routes(app):
    @app.route("/")
    def hello_world():
        return "Hello world"

    @app.route("/runs")
    def runs():
        return render_template("runs.html", runs=app.config["data"].runs(), type=type)
