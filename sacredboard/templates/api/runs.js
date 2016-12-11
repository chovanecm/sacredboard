{
    "draw": {{draw}},
    "recordsTotal": {{recordsTotal}},
    "recordsFiltered": {{recordsFiltered}},
    "data": [
    {% autoescape false %}
     {%- for run in runs -%}
    {
        "experiment_name": {{run.experiment.name | default | tojson}},
        "status": {{run.status | default  | tojson | safe}},
        "start_time": {{run.start_time | default  | format_datetime | tojson}},
        "heartbeat": {{run.heartbeat | default  | format_datetime | tojson}},
        "heartbeat_diff": {{run.heartbeat | default  | timediff | tojson}},
        "hostname": {{run.host.hostname | default  | tojson}},
        "captured_out_last_line": {{run.captured_out | default  | last_line | tojson}},
        "result":{{run.result | default | tojson}}
    }
        {%- if not loop.last -%}
            ,
        {% endif %}
    {% endfor %}
    {% endautoescape %}
    ]

}