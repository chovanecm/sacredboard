# coding=utf-8
import bson
import pymongo


class PyMongoDataAccess:
    """ Access records in MongoDB. """

    RUNNING_DEAD_RUN_CLAUSE = {"status": "RUNNING", "$where": "new Date() - this.heartbeat > 120000"}
    RUNNING_NOT_DEAD_CLAUSE = {"status": "RUNNING", "$where": "new Date() - this.heartbeat <= 120000"}
    def __init__(self, uri, database_name, collection_name):

        self._uri = uri
        self._db_name = database_name
        self._client = None
        self._db = None
        self._collection_name = collection_name

    def connect(self):
        self._client = self._create_client()
        self._db = getattr(self._client, self._db_name)

    def _create_client(self):
        """ Returns a new Mongo Client """
        return pymongo.MongoClient(host=self._uri)

    def get_runs(self, sort_by=None, sort_direction=None, start=0, limit=None, query={"type": "and", "filters": []}):
        mongo_query = self._to_mongo_query(query)
        cursor = getattr(self._db, self._collection_name).find(mongo_query)
        if sort_by is not None:
            cursor = self._apply_sort(cursor, sort_by, sort_direction)
        cursor = cursor.skip(start)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor

    def get_run(self, run_id):
        try:
            cursor = getattr(self._db, self._collection_name) \
                .find({"_id": int(run_id)})
        except ValueError:
            # Probably not a number.
            cursor = getattr(self._db, self._collection_name) \
                .find({"_id": bson.ObjectId(run_id)})
        run = None
        for c in cursor:
            run = c
        return run

    @staticmethod
    def _apply_sort(cursor, sort_by, sort_direction):
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

    @staticmethod
    def _to_mongo_query(query):
        """
        Takes a query in format
        [{field: 'host.hostname', operator: 'contains', value: 'asus'},
        {field: 'config.seed', operator: '==', value: 123},
        ]
        and returns mongo query like
        {"host.hostname": "asus", "config.seed": 123}
        :param query:
        :type query:
        :return:
        :rtype:
        """
        mongo_query = []
        for clause in query["filters"]:
            if clause.get("type") is None:
                # It's a regular clause
                mongo_clause = {}
                value = clause["value"]

                if clause["field"] == "status" and clause["value"] == "DEAD":
                    mongo_clause = PyMongoDataAccess.RUNNING_DEAD_RUN_CLAUSE
                    if clause["operator"] == "!=":
                        mongo_clause = {"$not": mongo_clause}
                elif clause["field"] == "status" and clause["value"] == "RUNNING":
                    mongo_clause = PyMongoDataAccess.RUNNING_NOT_DEAD_CLAUSE
                    if clause["operator"] == "!=":
                        mongo_clause = {"$not": mongo_clause}
                elif clause["operator"] == "==":
                    mongo_clause[clause["field"]] = value
                elif clause["operator"] == ">":
                    mongo_clause[clause["field"]] = {"$gt": value}
                elif clause["operator"] == ">=":
                    mongo_clause[clause["field"]] = {"$gte": value}
                elif clause["operator"] == "<":
                    mongo_clause[clause["field"]] = {"$lt": value}
                elif clause["operator"] == "<=":
                    mongo_clause[clause["field"]] = {"$lte": value}
                elif clause["operator"] == "!=":
                    mongo_clause[clause["field"]] = {"$ne": value}
                elif clause["operator"] == "regex":
                    mongo_clause[clause["field"]] = {"$regex": value}
            else:
                # It's a subclause
                mongo_clause = PyMongoDataAccess._to_mongo_query(clause)
            mongo_query.append(mongo_clause)

        if len(mongo_query) == 0:
            return {}
        if query["type"] == "and":
            return {"$and": mongo_query}
        elif query["type"] == "or":
            return {"$or": mongo_query}
        else:
            raise ValueError("Unexpected query type %s" % query.get("type"))


    @staticmethod
    def build_data_access(host, port, database_name, collection_name):
        """
       :param host: The database server to connect to
       :type host: str
       :param port: Database port
       :type port: int
       :param database_name: Database name
       :type database_name: str
       :param collection_name: Name of the collection
        where Sacred stores its runs
       :type collection_name: str
               """
        return PyMongoDataAccess("mongodb://%s:%d" % (host, port),
                                 database_name, collection_name)

    @staticmethod
    def build_data_access_with_uri(uri, database_name, collection_name):
        """
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

