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

    def runs(self):
        return self._db.runs.find()
