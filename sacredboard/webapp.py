from flask import Flask
from flask import render_template
from flask import jsonify
from bson.json_util import dumps

import click
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world"


@app.route("/api/runs")
def api_runs():
    import pymongo
    client = pymongo.MongoClient(host=app.config["mongo"]["host"], port=app.config["mongo"]["port"])
    db = getattr(client, app.config["mongo"]["db"])
    results = list(db.default.runs.find())
    return dumps(results)


@app.route("/runs")
def runs():
    import pymongo
    client = pymongo.MongoClient(host=app.config["mongo"]["host"], port=app.config["mongo"]["port"])
    db = getattr(client, app.config["mongo"]["db"])
    return render_template("runs.html", runs=db.runs.find(), type=type)


@app.template_filter("timediff")
def timediff(time):
    import datetime
    now = datetime.datetime.now()
    diff = now - time
    diff_sec = diff.total_seconds()
    return diff_sec


@click.command()
@click.option("--debug", is_flag=True, default=False)
@click.option("-m", default="sacred")
def run(debug, m):
    add_mongo_config(app, m)
    app.config['DEBUG'] = debug
    app.run(host="0.0.0.0", debug=debug)


def add_mongo_config(app, connection_string):
    split_string = connection_string.split(":")
    config = {"host": "localhost", "port": 27017, "db": "sacred"}
    if len(split_string) > 0:
        config["db"] = split_string[-1]
    if len(split_string) > 1:
        config["port"] = int(split_string[-2])
    if len(split_string) > 2:
        config["host"] = split_string[-3]
    app.config["mongo"] = config

if __name__ == '__main__':
    run()
