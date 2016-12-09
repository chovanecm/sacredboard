from flask import render_template
import pymongo


def setup_routes(app):
    @app.route("/")
    def hello_world():
        return "Hello world"

    @app.route("/runs")
    def runs():
        client = pymongo.MongoClient(host=app.config["mongo"]["host"], port=app.config["mongo"]["port"])
        db = getattr(client, app.config["mongo"]["db"])
        return render_template("runs.html", runs=db.runs.find(), type=type)
