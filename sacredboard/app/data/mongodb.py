import pymongo


class PyMongoDataAccess:

    def __init__(self, host, port, db):
        self._host = host
        self._port = port
        self._db_name = db
        self._client = None

    def connect(self):
        self._client = pymongo.MongoClient(host=self._host, port=self._port)
        self._db = getattr(self._client, self._db_name)

    def runs(self, sort_by=None, sort_direction=None, start=0, limit=None):
        cursor = self._db.runs.find()
        if (sort_by is not None):
            cursor =  self._apply_sort(cursor, sort_by, sort_direction)
        cursor = cursor.skip(start)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor


    def _apply_sort(self, cursor, sort_by, sort_direction):
        """
        :type sort_direction: str
        :return:
        :rtype: pymongo.Cursor
        """
        return cursor.sort(sort_by, pymongo.DESCENDING if sort_direction is not None
                                                          and sort_direction.lower() == "desc" else pymongo.ASCENDING)

