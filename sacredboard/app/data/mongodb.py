# coding=utf-8
import bson
import pymongo


class PyMongoDataAccess:
    """ Access records in MongoDB. """
    def __init__(self, host, port, db, collection_name):
        """

        :param host: The database server to connect to
        :type host: str
        :param port: Database port
        :type port: int
        :param db: Database name
        :type db: str
        :param collection_name: Name of the collection
         where Sacred stores its runs
        :type collection_name: str
        """
        self._host = host
        self._port = port
        self._db_name = db
        self._client = None
        self._db = None
        self._collection_name = collection_name

    def connect(self):
        self._client = pymongo.MongoClient(host=self._host, port=self._port)
        self._db = getattr(self._client, self._db_name)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None):
        cursor = getattr(self._db, self._collection_name).find()
        if sort_by is not None:
            cursor = self._apply_sort(cursor, sort_by, sort_direction)
        cursor = cursor.skip(start)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor

    def get_run(self, run_id):
        try:
            cursor = getattr(self._db, self._collection_name)\
                .find({"_id": int(run_id)})
        except ValueError:
            # Probably not a number.
            cursor = getattr(self._db, self._collection_name)\
                .find({"_id": bson.ObjectId(run_id)})
        run = None
        for c in cursor:
            run = c
        return run

    def _apply_sort(self, cursor, sort_by, sort_direction):
        """
        :type sort_direction: str
        :return:
        :rtype: pymongo.Cursor
        """
        if sort_direction is not None and sort_direction.lower() == "desc":
            sort = pymongo.DESCENDING
        else:
            sort = pymongo.ASCENDING
        return cursor.sort(sort_by, sort)
