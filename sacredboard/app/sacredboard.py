# coding=utf-8
"""Module for handling core functions linked to sacredboard itself."""

import pkg_resources # used to fetch the version number

class sacredboard():

    @staticmethod
    def get_version():
        """Returns the current version of sacredboard."""
        version = pkg_resources.require("sacredboard")[0].version
        return version
