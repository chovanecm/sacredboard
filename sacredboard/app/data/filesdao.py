"""
Interface for accessing Sacred files.
"""


class FilesDAO:
    """
    Interface for accessing files.
    """

    def get(self, file_id):
        """
        Return the file associated with the id.

        :raise NotFoundError when not found
        """
        raise NotImplementedError("RunDAO is abstract.")
