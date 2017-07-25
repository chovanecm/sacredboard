# coding=utf-8
"""Accesses data in Sacred's MongoDB."""
import pymongo

from sacredboard.app.data.datastorage import Cursor, DataStorage
from sacredboard.app.data.pymongo import GenericDAO, MongoMetricsDAO
from sacredboard.app.data.pymongo.rundao import MongoRunDAO


class MongoDbCursor(Cursor):
    """Implements Cursor for mongodb."""

    def __init__(self, mongodb_cursor):
        """Initialize a MongoDB cursor."""
        self.mongodb_cursor = mongodb_cursor

    def count(self):
        """Return the number of items in this cursor."""
        return self.mongodb_cursor.count()

    def __iter__(self):
        """Iterate over runs."""
        return self.mongodb_cursor


class PyMongoDataAccess(DataStorage):
    """Access records in MongoDB."""

    def __init__(self, uri, database_name, collection_name):
        """
        Set up MongoDB access layer, don't connect yet.

        Better use the static methods build_data_access
        or build_data_access_with_uri
        """
        super().__init__()
        self._uri = uri
        self._db_name = database_name
        self._client = None
        self._db = None
        self._collection_name = collection_name
        self._generic_dao = None

    def connect(self):
        """Initialize the database connection."""
        self._client = self._create_client()
        self._db = getattr(self._client, self._db_name)
        self._generic_dao = GenericDAO(self._client, self._db_name)

    def _create_client(self):
        """Return a new Mongo Client."""
        return pymongo.MongoClient(host=self._uri)

    def get_runs(self, *args, **kwargs):
        """
        Get runs.

        .. deprecated:: 0.3
            Use get_run_dao().get_runs instead.
        """
        return self.get_run_dao().get_runs(*args, **kwargs)

    def get_run(self, run_id):
        """
        Get a single run from the database.

        :param run_id: The ID of the run.
        :return: The whole object from the database.

        .. deprecated:: 0.3
            Use get_run_dao().get_runs instead.
        """
        return self.get_run_dao().get_run(run_id)

    @staticmethod
    def build_data_access(host, port, database_name, collection_name):
        """
        Create data access gateway.

        :param host: The database server to connect to.
        :type host: str
        :param port: Database port.
        :type port: int
        :param database_name: Database name.
        :type database_name: str
        :param collection_name: Name of the collection with Sacred runs.
        :type collection_name: str
        """
        return PyMongoDataAccess("mongodb://%s:%d" % (host, port),
                                 database_name, collection_name)

    @staticmethod
    def build_data_access_with_uri(uri, database_name, collection_name):
        """
        Create data access gateway given a MongoDB URI.

        :param uri: Connection string as defined in
                https://docs.mongodb.com/manual/reference/connection-string/
        :type uri: str
        :param database_name: Database name
        :type database_name: str
        :param collection_name: Name of the collection
        where Sacred stores its runs
        :type collection_name: str
        """
        return PyMongoDataAccess(uri, database_name, collection_name)

    def get_metrics_dao(self):
        """
        Return a data access object for metrics.

        The method can be called only after a connection to DB is established.
        Issue: https://github.com/chovanecm/sacredboard/issues/62

        :return MetricsDAO
        """
        return MongoMetricsDAO(self._generic_dao)

    def get_run_dao(self):
        """
        Return a data access object for Runs.

        :return: RunDAO
        """
        return MongoRunDAO(self._generic_dao, self._collection_name)
