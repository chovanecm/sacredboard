"""Interface for accessing Sacred files."""
import datetime
import typing


class FilesDAO:
    """Interface for accessing files."""

    def get(self, file_id) -> [typing.BinaryIO, str, datetime.datetime]:
        """
        Return the file associated with the id as binary stream and its filename and upload date.
        :raise NotFoundError when not found
        """
        raise NotImplementedError("RunDAO is abstract.")
