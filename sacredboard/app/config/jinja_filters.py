# coding=utf-8
"""
Configures filters for use in pages rendered by Flask.

It helps writing the frontend templates,
 e.g. a data variable can be rendered in local format using
 {{date_variable | format_datetime}}
"""
import datetime

import simplejson
from bson import json_util
from flask import Blueprint

filters = Blueprint("filters", __name__)


@filters.app_template_filter("format_datetime")
def format_datetime(value):
    """Format datetime according to server's locale."""
    return value.strftime('%X %x')


@filters.app_template_filter("timediff")
def timediff(time):
    """Return the difference in seconds between now and the given time."""
    now = datetime.datetime.utcnow()
    diff = now - time
    diff_sec = diff.total_seconds()
    return diff_sec


@filters.app_template_filter("last_line")
def last_line(text):
    """
    Get the last meaningful line of the text, that is the last non-empty line.

    :param text: Text to search the last line
    :type text: str
    :return:
    :rtype: str
    """
    last_line_of_text = ""
    while last_line_of_text == "" and len(text) > 0:
        last_line_start = text.rfind("\n")
        # Handle one-line strings (without \n)
        last_line_start = max(0, last_line_start)
        last_line_of_text = text[last_line_start:].strip("\r\n ")
        text = text[:last_line_start]
    return last_line_of_text


@filters.app_template_filter("first_letter")
def first_letter(text):
    """Return the first leter of the text."""
    return text[:1]


@filters.app_template_filter("dump_json")
def dump_json(obj):
    """Dump Python object as JSON string."""
    return simplejson.dumps(obj, ignore_nan=True, default=json_util.default)


@filters.app_template_filter("tostr")
def tostr(obj):
    """Convert object to string."""
    return str(obj)


@filters.app_template_filter("detect_alive_experiment")
def detect_alive_experiment(time_difference):
    """Decide whether experiment is alive or not."""
    return time_difference < 120


def initialize(app):
    """Register the filters in a Flask application."""
    app.register_blueprint(filters)
