def setup_filters(app):
    @app.template_filter("format_datetime")
    def format_datetime(value):
        return value.strftime('%X %x')

    @app.template_filter("timediff")
    def timediff(time):
        import datetime
        now = datetime.datetime.now()
        diff = now - time
        diff_sec = diff.total_seconds()
        return diff_sec
