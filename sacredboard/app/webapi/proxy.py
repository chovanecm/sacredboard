"""
Reverse proxy support for Sacredboard.

http://blog.macuyiko.com/post/2016/fixing-flask-url_for-when-behind-mod_proxy.html
"""
from flask import Flask


class ReverseProxied(object):
    """
    Allow to use a reverse proxy.

    http://blog.macuyiko.com/post/2016/fixing-flask-url_for-when-behind-mod_proxy.html
    """

    def __init__(self, app, script_name=None, scheme=None, server=None):
        """Create a new wrapper for Flask."""
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        """Set environment for Flask."""
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


def initialize(app: Flask, app_config):
    """
    Initialize the module.

    :param app: The Flask application.
    :param app_config: Application configuration dictionary. If `http.serve_on_endpoint` attribute
     is specified (e.g. /sacredboard/), the application will be hosted on that endpoint
    (e.g. http://localhost:5000/sacredboard/)
    """
    sub_url = app_config["http.serve_on_endpoint"]
    if sub_url is not "/":
        app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=sub_url)
