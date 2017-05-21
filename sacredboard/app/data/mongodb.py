# coding=utf-8
"""Accesses data in Sacred's MongoDB."""
import bson
import pymongo


class PyMongoDataAccess:
    """Access records in MongoDB."""

    RUNNING_DEAD_RUN_CLAUSE = {
        "status": "RUNNING", "$where": "new Date() - this.heartbeat > 120000"}
    RUNNING_NOT_DEAD_CLAUSE = {
        "status": "RUNNING", "$where": "new Date() - this.heartbeat <= 120000"}

    def __init__(self, uri, database_name, collection_name):
        """
        Set up MongoDB access layer, don't connect yet.

        Better use the static methods build_data_access
        or build_data_access_with_uri
        """
        self._uri = uri
        self._db_name = database_name
        self._client = None
        self._db = None
        self._collection_name = collection_name

    def connect(self):
        """Initialize the database connection."""
        self._client = self._create_client()
        self._db = getattr(self._client, self._db_name)

    def _create_client(self):
        """Return a new Mongo Client."""
        return pymongo.MongoClient(host=self._uri)

    def get_runs(self, sort_by=None, sort_direction=None,
                 start=0, limit=None, query={"type": "and", "filters": []}):
        """
        Return multiple runs (default all).

        The query format (optional):

        {"type": "and", "filters": [
         {"field": "host.hostname", "operator": "==", "value": "ntbacer"},
         {"type": "or", "filters": [
            {"field": "result", "operator": "==", "value": 2403.52},
            {"field": "host.python_version", "operator": "==", "value":"3.5.2"}
            ]}]}

        The parameter is built from clauses.
        Each clause is either conjunctive (``"and"``), disjunctive (``"or"``),
        or a *terminal clause*. Each of the the earlier two types must specify
        the ``"filters`` array of other clauses to be joined together
        by that logical connective (and/or).

        A terminal clause does not specifies its type, instead,
        it has a different set of fields:
        the ``field`` to be queried on (based on the MongoDB schema,
        using dot notation to access nested documents), the ``operator``
        (one of ``"=="``, ``"!="``, ``"<"``, ``"<="``, ``">``, ``">="``,
        and ``"regex"`` for regular expressions).
        The ``value`` field contains the value to be compared with
        (either a string or a number).
        Notice that for the ``status`` field, the ``RUNNING`` and ``DEAD`` runs
        are compared by :func:`~PyMongoDataAccess.RUNNING_DEAD_RUN_CLAUSE` and
        :func:`~PyMongoDataAccess.RUNNING_NOT_DEAD_CLAUSE`
        """
        mongo_query = self._to_mongo_query(query)
        cursor = getattr(self._db, self._collection_name).find(mongo_query)
        if sort_by is not None:
            cursor = self._apply_sort(cursor, sort_by, sort_direction)
        cursor = cursor.skip(start)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor

    def get_run(self, run_id):
        """
        Get a single run from the database.
        
        :param run_id: The ID of the run.
        :return: The whole object from the database.
        """
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

    @staticmethod
    def _to_mongo_query(query):
        """
        Convert the query received by the Sacred Web API to a MongoDB query.
        
        Takes a query in format
        {"type": "and", "filters": [
         {"field": "host.hostname", "operator": "==", "value": "ntbacer"},
         {"type": "or", "filters": [
            {"field": "result", "operator": "==", "value": 2403.52},
            {"field": "host.python_version", "operator": "==", "value":"3.5.2"}
            ]}]}
        and returns an appropriate MongoDB Query.
        :param query: A query in the Sacred Web API format.
        :return: Mongo Query.
        """
        mongo_query = []
        for clause in query["filters"]:
            if clause.get("type") is None:
                mongo_clause = PyMongoDataAccess. \
                    _simple_clause_to_query(clause)
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
    def _simple_clause_to_query(clause):
        """
        Convert a clause from the Sacred Web API format to the MongoDB format.
        
        :param clause: A clause to be converted. It must have "field",
        "operator" and "value" fields.
        :return: A MongoDB clause.
        """
        # It's a regular clause
        mongo_clause = {}
        value = clause["value"]
        if clause["field"] == "status" and \
           clause["value"] in ["DEAD", "RUNNING"]:
            return PyMongoDataAccess.\
                _status_filter_to_query(clause)
        if clause["operator"] == "==":
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
        return mongo_clause

    @staticmethod
    def _status_filter_to_query(clause):
        """
        Convert a clause querying for an experiment state RUNNING or DEAD.
        
        Queries that check for experiment state RUNNING and DEAD need to be
        replaced by the logic that decides these two states as both of them
        are stored in the Mongo Database as "RUNNING". We use querying by last
        heartbeat time.
        
        :param clause: A clause whose field is "status" and "value" is one of 
        RUNNING, DEAD.
        :return: A MongoDB clause.
        """
        if clause["value"] == "RUNNING":
            mongo_clause = PyMongoDataAccess.RUNNING_NOT_DEAD_CLAUSE
        elif clause["value"] == "DEAD":
            mongo_clause = PyMongoDataAccess.RUNNING_DEAD_RUN_CLAUSE
        if clause["operator"] == "!=":
            mongo_clause = {"$not": mongo_clause}
        return mongo_clause

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
