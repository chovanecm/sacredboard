# coding=utf-8
"""
Bootstrap module parses command line arguments and initializes the app.

Configures the database connection and starts the web application.
"""
import locale
import sys

import click
from flask import Flask
from gevent.pywsgi import WSGIServer

from sacredboard.app.config import jinja_filters
from sacredboard.app.data.filestorage import FileStorage
from sacredboard.app.data.mongodb import PyMongoDataAccess
from sacredboard.app.webapi import routes, metrics, runs

locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)

webapi_modules = [routes, metrics, runs, jinja_filters]


@click.command()
@click.option("-m", default=None, metavar="HOST:PORT:DATABASE",
              help="Connect to MongoDB using the format"
                   " host:port:database_name or just the database_name. "
                   "Default: sacred"
                   " Mutually exclusive with -mu")
@click.option("-mu", default=(None, None),
              metavar="CONNECTION_STRING DATABASE", type=(str, str),
              help="Connect to MongoDB using mongodb://..."
                   " and specify the database name."
                   " Mutually exclusive with -m")
@click.option("-mc", default="runs", metavar="COLLECTION",
              help="The collection containing the Sacred's list of runs. "
                   "You might need it if you use a custom collection name "
                   "or Sacred v0.6 (which used default.runs). "
                   "Default: runs")
@click.option("-F", default="",
              help="Path to directory containing experiment results of the"
                   "File Storage observer. (experimental)")
@click.option("--no-browser", is_flag=True, default=False,
              help="Do not open web browser automatically.")
@click.option("--debug", is_flag=True, default=False,
              help="Run the application in Flask debug mode "
                   "(for development).")
@click.version_option()
def run(debug, no_browser, m, mu, mc, f):
    """
    Sacredboard.

\b
Sacredboard is a monitoring dashboard for Sacred.
Homepage: http://github.com/chovanecm/sacredboard

Example usage:

\b
sacredboard -m sacred
    Starts Sacredboard on default port (5000) and connects to
    a local MongoDB database called 'sacred'. Opens web browser.
    Note: MongoDB must be listening on localhost.
\b
sacredboard -m 192.168.1.1:27017:sacred
    Starts Sacredboard on default port (5000) and connects to
    a MongoDB database running on 192.168.1.1 on port 27017
    to a database called 'sacred'. Opens web browser.
\b
sacredboard -mu mongodb://user:pwd@host/admin?authMechanism=SCRAM-SHA-1 sacred
    Starts Sacredboard on default port (5000) and connects to
    a MongoDB database running on localhost on port 27017
    to a database called 'sacred'. Opens web browser.

\b
sacredboard -m sacred -mc default.runs
    Starts Sacredboard on default port (5000) and connects to
    a local MongoDB database called 'sacred' and uses the Sacred's 0.6
    default collection 'default.runs' to search the runs in.
    Opens web browser.
    Note: MongoDB must be listening on localhost.

    """
    if m or mu != (None, None):
        add_mongo_config(app, m, mu, mc)
        app.config["data"].connect()
    elif f:
        app.config["data"] = FileStorage(f)
    else:
        print("Must specify either a mongodb instance or " +
              "a path to a file storage.\nRun sacredboard --help "
              "for more information.", file=sys.stderr)
        sys.exit(1)

    app.config['DEBUG'] = debug
    app.debug = debug

    for module in webapi_modules:
        # Initialize Web Api Modules
        module.initialize(app)

    if debug:
        app.run(host="0.0.0.0", debug=True)
    else:
        for port in range(5000, 5050):
            http_server = WSGIServer(('0.0.0.0', port), app)
            try:
                http_server.start()
            except OSError as e:
                # try next port
                continue
            print("Starting sacredboard on port %d" % port)
            if not no_browser:
                click.launch("http://127.0.0.1:%d" % port)
            http_server.serve_forever()
            break


def add_mongo_config(app, simple_connection_string,
                     mongo_uri, collection_name):
    """
    Configure the application to use MongoDB.

    :param app: Flask application
    :param simple_connection_string:
                Expects host:port:database_name or database_name
                Mutally_exclusive with mongo_uri
    :param mongo_uri: Expects mongodb://... as defined
                in https://docs.mongodb.com/manual/reference/connection-string/
                Mutually exclusive with simple_connection_string (must be None)
    :param collection_name: The collection containing Sacred's runs
    :return:
    """
    if mongo_uri != (None, None):
        add_mongo_config_with_uri(app, mongo_uri[0], mongo_uri[1],
                                  collection_name)
        if simple_connection_string is not None:
            print("Ignoring the -m option. Overridden by "
                  "a more specific option (-mu).", file=sys.stderr)
    else:
        # Use the default value 'sacred' when not specified
        if simple_connection_string is None:
            simple_connection_string = "sacred"
        add_mongo_config_simple(app, simple_connection_string, collection_name)


def add_mongo_config_simple(app, connection_string, collection_name):
    """
    Configure the app to use MongoDB.

    :param app: Flask Application
    :type app: Flask
    :param connection_string: in format host:port:database or database
            (default: sacred)
    :type connection_string: str

    :param collection_name: Name of the collection
    :type collection_name: str
    """
    split_string = connection_string.split(":")
    config = {"host": "localhost", "port": 27017, "db": "sacred"}
    if len(split_string) > 0 and len(split_string[-1]) > 0:
        config["db"] = split_string[-1]
    if len(split_string) > 1:
        config["port"] = int(split_string[-2])
    if len(split_string) > 2:
        config["host"] = split_string[-3]
    app.config["data"] = PyMongoDataAccess.build_data_access(
        config["host"], config["port"], config["db"], collection_name)


def add_mongo_config_with_uri(app, connection_string_uri,
                              database_name, collection_name):
    """
    Configure PyMongo with a MongoDB connection string.

    :param app: Flask application
    :param connection_string_uri: MongoDB connection string
    :param database_name: Sacred database name
    :param collection_name: Sacred's collection with runs
    :return:
    """
    app.config["data"] = PyMongoDataAccess.build_data_access_with_uri(
        connection_string_uri, database_name, collection_name
    )


if __name__ == '__main__':
    run()
