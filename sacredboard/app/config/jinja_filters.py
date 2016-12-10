import datetime
from flask import Blueprint

filters = Blueprint("filters", __name__)


@filters.app_template_filter("format_datetime")
def format_datetime(value):
    return value.strftime('%X %x')


format_datetime


@filters.app_template_filter("timediff")
def timediff(time):
    now = datetime.datetime.now()
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
    last_line = ""
    while last_line == "" and len(text) > 0:
        last_line_start = text.rfind("\n")
        # Handle one-line strings (without \n)
        last_line_start = max(0, last_line_start)
        last_line = text[last_line_start:].strip("\r\n ")
        text = text[:last_line_start]
    return last_line


@filters.app_template_filter("first_letter")
def first_letter(text):
    return text[:1]


def setup_filters(app):
    app.register_blueprint(filters)
