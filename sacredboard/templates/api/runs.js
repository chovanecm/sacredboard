{
    "draw": {{draw}},
    "recordsTotal": {{recordsTotal}},
    "recordsFiltered": {{recordsFiltered}},
    "data": [
    {% autoescape false %}
     {% for run in runs %}
    {
        "experiment_name": {{run.experiment.name | tojson}},
        "status": {{run.status | tojson | safe}},
        "start_time": {{run.start_time | format_datetime | tojson}},
        "heartbeat": {{run.heartbeat | format_datetime | tojson}},
        "heartbeat_diff": {{run.heartbeat | timediff | tojson}},
        "hostname": {{run.host.hostname | tojson}},
        "captured_out_last_line": {{run.captured_out | last_line | tojson}},
        "result":"{{run.result}}"
    }
        {% if not loop.last %}
            ,
        {% endif %}
    {% endfor %}
    {% endautoescape %}
    ]

}