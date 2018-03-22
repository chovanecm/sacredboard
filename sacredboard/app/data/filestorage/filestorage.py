"""Implements backend storage interface for sacred's file store."""

import os

from sacredboard.app.data.datastorage import DataStorage
from sacredboard.app.data.filestorage.rundao import FileStoreRunDAO
from sacredboard.app.data.rundao import RunDAO


class FileStorage(DataStorage):
    """Object to interface with one of sacred's file stores."""

    def get_run_dao(self) -> RunDAO:
        """Return the Data Access Object for manipulating runs."""
        return FileStoreRunDAO(self.path_to_dir)

    def __init__(self, path_to_dir):
        """Initialize file storage run accessor."""
        super().__init__()
        self.path_to_dir = os.path.expanduser(path_to_dir)
