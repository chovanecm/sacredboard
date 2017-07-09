# coding=utf-8
"""WebAPI module for handling run-related requests."""
import json

from flask import current_app, request, Response, render_template


def parse_int_arg(name, default):
    """Return a given URL parameter as int or return the default value."""
    return default if request.args.get(name) is None \
        else int(request.args.get(name))


def parse_query_filter():
    """Parse the Run query filter from the URL as a dictionary."""
    query_string = request.args.get("queryFilter")
    if query_string is None:
        return {"type": "and", "filters": []}
    query = json.loads(query_string)
    assert type(query) == dict
    assert type(query.get("type")) == str
    return query


def get_runs():
    """Get all runs, sort it and return a response."""
    data = current_app.config["data"]
    draw = parse_int_arg("draw", 1)
    start = parse_int_arg("start", 0)
    length = parse_int_arg("length", -1)
    length = length if length >= 0 else None
    order_column = request.args.get("order[0][column]")
    order_dir = request.args.get("order[0][dir]")

    query = parse_query_filter()

    if order_column is not None:
        order_column = \
            request.args.get("columns[%d][name]" % int(order_column))
        if order_column == "hostname":
            order_column = "host.hostname"

    runs = data.get_runs(
        start=start, limit=length,
        sort_by=order_column, sort_direction=order_dir, query=query)
    # records_total should be the total size of the records in the database,
    # not what was returned
    records_total = runs.count()
    records_filtered = runs.count()
    return Response(render_template(
        "api/runs.js", runs=runs,
        draw=draw, recordsTotal=records_total,
        recordsFiltered=records_filtered),
        mimetype="application/json")
