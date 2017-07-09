"""
Generic DAO object for safe access to the MongoDB.

Issue: https://github.com/chovanecm/sacredboard/issues/61
"""
import pymongo
from pymongo.errors import InvalidName

from sacredboard.app.data import DataSourceError
from .mongocursor import MongoDbCursor


class GenericDAO:
    """
    Generic DAO object for safe access to the MongoDB.

    Issue: https://github.com/chovanecm/sacredboard/issues/61
    """

    def __init__(self, pymongo_client, database_name):
        """
        Create a new GenericDAO object that will work on the given database.

        :param pymongo_client: PyMongo client that is connected to MongoDB.
        :param database_name: Name of the database this GenericDAO works with.

        :raise DataSourceError
        """
        self._client = pymongo_client
        self._database = self._get_database(database_name)

    def find_record(self, collection_name, query):
        """
        Return the first record mathing the given Mongo query.

        :param collection_name: Name of the collection to search in.
        :param query: MongoDB Query, e.g. {_id: 123}
        :return: A single MongoDB record or None if not found.

        :raise DataSourceError
        """
        cursor = self._get_collection(collection_name).find(query)
        for record in cursor:
            # Return the first record found.
            return record
        # Return None if nothing found.
        return None

    def find_records(self, collection_name, query={}, sort_by=None,
                     sort_direction=None, start=0, limit=None):
        """
        Return a cursor of records from the given MongoDB collection.

        :param collection_name: Name of the MongoDB collection to query.
        :param query: Standard MongoDB query. By default no restriction.
        :param sort_by: Name of a single field to sort by.
        :param sort_direction: The direction to sort, "asc" or "desc".
        :param start: Skip first n results.
        :param limit: The maximum number of results to return.

        :return: Cursor -- An iterable with results.
        :raise DataSourceError
        """
        cursor = self._get_collection(collection_name).find(query)
        if sort_by is not None:
            cursor = self._apply_sort(cursor, sort_by, sort_direction)
        cursor = cursor.skip(start)
        if limit is not None:
            cursor = cursor.limit(limit)
        return MongoDbCursor(cursor)

    def delete_record(self, collection_name, query):
        """Delete record matching the given MongoDB query."""
        return self._get_collection(collection_name).remove(query)

    def _get_database(self, database_name):
        """
        Get PyMongo client pointing to the current database.

        :return: MongoDB client of the current database.
        :raise DataSourceError
        """
        try:
            return self._client[database_name]
        except InvalidName as ex:
            raise DataSourceError("Cannot connect to database %s!"
                                  % self._database) from ex

    def _get_collection(self, collection_name):
        """
        Get PyMongo client pointing to the current DB and the given collection.

        :return: MongoDB client of the current database and given collection.
        :raise DataSourceError
        """
        try:
            return self._database[collection_name]
        except InvalidName as ex:
            raise DataSourceError("Cannot access MongoDB collection %s!"
                                  % collection_name) from ex
        except Exception as ex:
            raise DataSourceError("Unexpected error when accessing MongoDB"
                                  "collection %s!"
                                  % collection_name) from ex

    def _apply_sort(self, cursor, sort_by, sort_direction):
        """
        Apply sort to a cursor.

        :param cursor: The cursor to apply sort on.
        :param sort_by: The field name to sort by.
        :param sort_direction: The direction to sort, "asc" or "desc".
        :return:

        """
        if sort_direction is not None and sort_direction.lower() == "desc":
            sort = pymongo.DESCENDING
        else:
            sort = pymongo.ASCENDING
        return cursor.sort(sort_by, sort)
