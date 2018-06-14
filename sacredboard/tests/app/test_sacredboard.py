from unittest import TestCase

from sacredboard.app.sacredboard import Sacredboard


class TestSacredboard(TestCase):
    def test_get_version(self):
        assert Sacredboard.get_version() == "0.4.1.dev5"
