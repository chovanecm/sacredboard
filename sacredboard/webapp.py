# coding=utf-8
import locale

import click
from flask import Flask
from gevent.pywsgi import WSGIServer

from sacredboard.app.config import jinja_filters
from sacredboard.app.config import routes
from sacredboard.app.data.mongodb import PyMongoDataAccess

locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)


@click.command()
@click.option("-m", default="sacred", metavar="CONNECTION_STRING",
              help="Connect to MongoDB on host:port:database or database. "
                   "Default: sacred")
@click.option("--no-browser", is_flag=True, default=False,
              help="Do not open web browser automatically.")
@click.option("--debug", is_flag=True, default=False,
              help="Run the application in Flask debug mode "
                   "(for development).")
@click.version_option()
def run(debug, no_browser, m):
    """
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

    """
    add_mongo_config(app, m)
    app.config['DEBUG'] = debug
    app.debug = debug
    jinja_filters.setup_filters(app)
    routes.setup_routes(app)
    app.config["data"].connect()
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


def add_mongo_config(app, connection_string):
    """
    Configure the app to use MongoDB.

    :param app: the Flask Application
    :type app: Flask
    :param connection_string: in format host:port:database or database
            (default: sacred)
    :type connection_string: str
    """
    split_string = connection_string.split(":")
    config = {"host": "localhost", "port": 27017, "db": "sacred"}
    if len(split_string) > 0 and len(split_string[-1]) > 0:
        config["db"] = split_string[-1]
    if len(split_string) > 1:
        config["port"] = int(split_string[-2])
    if len(split_string) > 2:
        config["host"] = split_string[-3]
    app.config["data"] = PyMongoDataAccess(
        config["host"], config["port"], config["db"])


if __name__ == '__main__':
    run()
