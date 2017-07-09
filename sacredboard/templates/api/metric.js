{
    "run_id": {{run_id}},
    "metric_id": "{{metric_id}}",
    "name": "{{name}}",
    "steps": {{steps}},
    "strtimestamps": [
        {%- for timestamp in timestamps -%}"{{timestamp | format_metric_timestamp}}"{%- if not loop.last -%}, {% endif %}{% endfor %}
        ],
    "values": {{values}}
}