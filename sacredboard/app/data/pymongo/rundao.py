"""
Module responsible for accessing the Metrics data in MongoDB.

Issue: https://github.com/chovanecm/sacredboard/issues/69
"""
import bson
import pymongo

from sacredboard.app.data.pymongo import GenericDAO
from sacredboard.app.data.rundao import RunDAO


class MongoRunDAO(RunDAO):
    """Implementation of MetricsDAO for MongoDB."""

    def __init__(self, generic_dao: GenericDAO, collection_name="runs"):
        """
        Create new Run accessor for MongoDB.

        :param generic_dao: A configured generic MongoDB data access object
         pointing to an appropriate database.
        :param collection_name: The collection to search runs in.
        """
        self.generic_dao = generic_dao
        self.collection_name = collection_name
        """Name of the MongoDB collection with Runs."""

    RUNNING_DEAD_RUN_CLAUSE = {
        "status": "RUNNING", "$where": "new Date() - this.heartbeat > 120000"}
    RUNNING_NOT_DEAD_CLAUSE = {
        "status": "RUNNING", "$where": "new Date() - this.heartbeat <= 120000"}

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
        (either a string or a number). Notice that for the ``status`` field,
        the ``RUNNING`` and ``DEAD`` runs are compared by
        :func:`~PyMongoDataAccess.RUNNING_DEAD_RUN_CLAUSE` and
        :func:`~PyMongoDataAccess.RUNNING_NOT_DEAD_CLAUSE`
        """
        mongo_query = self._to_mongo_query(query)
        r = self.generic_dao.find_records(self.collection_name, mongo_query,
                                          sort_by, sort_direction, start,
                                          limit)
        return r

    def get_run(self, run_id):
        """
        Get a single run from the database.

        :param run_id: The ID of the run.
        :return: The whole object from the database.
        """
        id = self._parse_id(run_id)

        run = self.generic_dao.find_record(self.collection_name,
                                           {"_id": id})
        return run

    def _parse_id(self, run_id):
        id = None
        try:
            id = int(run_id)
        except ValueError:
            id = bson.ObjectId(run_id)
        return id

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
                mongo_clause = MongoRunDAO. \
                    _simple_clause_to_query(clause)
            else:
                # It's a subclause
                mongo_clause = MongoRunDAO._to_mongo_query(clause)
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
        if clause["field"] == "status" and clause["value"] in ["DEAD",
                                                               "RUNNING"]:
            return MongoRunDAO. \
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
            mongo_clause = MongoRunDAO.RUNNING_NOT_DEAD_CLAUSE
        elif clause["value"] == "DEAD":
            mongo_clause = MongoRunDAO.RUNNING_DEAD_RUN_CLAUSE
        if clause["operator"] == "!=":
            mongo_clause = {"$not": mongo_clause}
        return mongo_clause

    def delete_run(self, run_id, run_only=False):
        """
        Delete run with the given id from the backend.

        :param run_id: Id of the run to delete.
        :param run_only: If true, only the run object is deleted. If false, the
        backend may delete additional related records as well.
        CURRENTLY ONLY THE RUN IS DELETED NO MATTER THE VALUE IS.
        :type bool
        :raise NotImplementedError If not supported by the backend.
        :raise DataSourceError General data source error.
        :raise NotFoundError The run was not found. (Some backends may succeed
        even if the run does not exist.
        """
        return self.generic_dao.delete_record(self.collection_name,
                                              self._parse_id(run_id))
