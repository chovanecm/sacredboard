"""Module responsible for accessing the Files data in MongoDB."""
import datetime
from typing import Union
import typing

import bson
import gridfs

from sacredboard.app.data.pymongo import GenericDAO
from sacredboard.app.data.filesdao import FilesDAO


class MongoFilesDAO(FilesDAO):
    """Implementation of FilesDAO for MongoDB."""

    def __init__(self, generic_dao: GenericDAO):
        """
        Create new Files accessor for MongoDB.

        :param generic_dao: A configured generic MongoDB data access object
         pointing to an appropriate database.
        """
        self.generic_dao = generic_dao

        self._fs = gridfs.GridFS(self.generic_dao._database)

    def get(self, file_id: Union[str, bson.ObjectId]) -> [typing.BinaryIO, str, datetime.datetime]:
        """
        Return the file identified by a file_id string.

        The return value is a file-like object which also has the following attributes:
        filename: str
        upload_date: datetime
        """
        if isinstance(file_id, str):
            file_id = bson.ObjectId(file_id)
        file = self._fs.get(file_id)
        return file, file.filename, file.upload_date
