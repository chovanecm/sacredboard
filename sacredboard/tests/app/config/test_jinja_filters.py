# coding=utf-8
import pytest

import sacredboard.app.config.jinja_filters as jf


@pytest.mark.parametrize("text", (
        "Last line", "Line1 \nLine2 \n Last line \n", "Last line\n",
        "\nLast line", "\nLast line\n", "\r\nLast line",
        "\r\nLast line\r\n"))
def test_last_line(text):
    result = jf.last_line(text)
    assert (result == "Last line")
