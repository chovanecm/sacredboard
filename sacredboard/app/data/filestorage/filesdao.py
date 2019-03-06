"""Module responsible for accessing the Files data in MongoDB."""
import datetime
import typing
from typing import Union

import bson
import gridfs

from sacredboard.app.data.pymongo import GenericDAO
from sacredboard.app.data.filesdao import FilesDAO


class FileStoreFilesDAO(FilesDAO):
    """Implementation of FilesDAO for MongoDB."""

    def __init__(self, generic_dao: GenericDAO):
        """
        Create new Files accessor for MongoDB.

        :param generic_dao: A configured generic MongoDB data access object
         pointing to an appropriate database.
        """

    def get(self, file_id: str) -> [typing.BinaryIO, str, datetime.datetime]:
        """
        Return the file identified by a file_id string, its file name and upload date

        """
        raise NotImplementedError("Downloading files for downloading files in FileStore has not been implemented yet.")
