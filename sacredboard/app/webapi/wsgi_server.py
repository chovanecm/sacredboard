# coding=utf-8
"""Module for starting the WSGI Server and the web application itself."""
from gevent.pywsgi import WSGIServer


class ServerRunner:
    """Sets up the HTTP server (WSGI, if not in debug mode) and runs it."""

    def __init__(self):
        """Once initialized, contains the port where the application will listen."""
        self.started_on_port = None

    def initialize(self, app, app_config):
        """Prepare the server to run and determine the port."""
        debug = app_config["debug"]
        port = app_config["http.port"]
        if debug:
            self.started_on_port = port
            app.run(host="0.0.0.0", debug=True, port=port)
        else:
            for port in range(port, port + 50):
                self.http_server = WSGIServer(('0.0.0.0', port), app)
                try:
                    self.http_server.start()
                except OSError as e:
                    # try next port
                    continue
                self.started_on_port = port
                break

    def run_server(self):
        """Start the server."""
        self.http_server.serve_forever()
