import locale

import click
from flask import Flask
from sacredboard.app.config import jinja_filters

from sacredboard.app.config import routes
from sacredboard.app.data.mongodb import PyMongoDataAccess

locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)


@click.command()
@click.option("--debug", is_flag=True, default=False)
@click.option("-m", default="sacred")
def run(debug, m):
    add_mongo_config(app, m)
    app.config['DEBUG'] = debug
    app.debug = debug
    jinja_filters.setup_filters(app)
    routes.setup_routes(app)
    app.config["data"].connect()
    app.run(host="0.0.0.0", debug=debug)


def add_mongo_config(app, connection_string):
    split_string = connection_string.split(":")
    config = {"host": "localhost", "port": 27017, "db": "sacred"}
    if len(split_string) > 0 and len(split_string[-1]) > 0:
        config["db"] = split_string[-1]
    if len(split_string) > 1:
        config["port"] = int(split_string[-2])
    if len(split_string) > 2:
        config["host"] = split_string[-3]
    app.config["data"] = PyMongoDataAccess(config["host"], config["port"], config["db"])

if __name__ == '__main__':
    run()
