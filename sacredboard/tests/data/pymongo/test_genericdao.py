import bson
import pytest
import flexmock

from sacredboard.app.data.datastorage import Cursor
from sacredboard.app.data.pymongo.genericdao import GenericDAO


def test_find_record_when_record_does_not_exist():
    test_query = {"_id": "NON_EXISTING_ID"}
    collection = flexmock()
    collection.should_receive("find").once().with_args(test_query).and_return([])
    mongo_client = {"testdb": {"runs": collection}}
    generic_dao = GenericDAO(mongo_client, "testdb")

    r = generic_dao.find_record("runs", test_query)

    assert r is None


def test_find_record():
    test_query = {"_id": bson.ObjectId("58163443b1758523257c69ca")}
    collection = flexmock()
    collection.should_receive("find").once().with_args(test_query).and_return([{"config": {"seed": 185616783}}])
    mongo_client = {"testdb": {"runs": collection}}
    generic_dao = GenericDAO(mongo_client, "testdb")

    r = generic_dao.find_record("runs", test_query)

    assert r is not None
    assert r["config"] is not None
    assert r["config"]["seed"] == 185616783


def test_find_records_in_empty_collection():
    mongo_cursor = flexmock()
    mongo_cursor.should_receive("skip").and_return(mongo_cursor)
    mongo_cursor.should_receive("__iter__").and_return(iter([]))
    #mongo_cursor.should_receive("__next__").and_raise(StopIteration)
    mongo_cursor.should_receive("count").and_return(0)
    collection = flexmock()
    collection.should_receive("find").once().with_args({}).and_return(mongo_cursor)
    mongo_client = {"testdb": {"EMPTY_COLLECTION": collection}}
    generic_dao = GenericDAO(mongo_client, "testdb")

    r = generic_dao.find_records("EMPTY_COLLECTION")

    assert isinstance(r, Cursor)
    assert r.count() == 0
    assert len(list(r)) == 0

def test_find_records_in_non_empty_collection(mongo_client):
    # Existing collection
    generic_dao = GenericDAO(mongo_client, "testdb")
    runs = list(generic_dao.find_records("runs"))
    assert len(runs) == 2
    assert runs[0]["host"]["hostname"] == "ntbacer"
    assert runs[1]["host"]["hostname"] == "martin-virtual-machine"


def test_find_records_limit(mongo_client):
    generic_dao = GenericDAO(mongo_client, "testdb")
    runs = list(generic_dao.find_records("runs", limit=1))
    assert len(runs) == 1, ""
    assert runs[0]["host"]["hostname"] == "ntbacer"


def test_find_records_order(mongo_client):
    generic_dao = GenericDAO(mongo_client, "testdb")
    runs = list(
        generic_dao.find_records("runs", sort_by="host.python_version"))
    assert len(runs) == 2
    assert runs[0]["host"]["python_version"] == "3.4.3"
    assert runs[1]["host"]["python_version"] == "3.5.2"

    runs = list(generic_dao.find_records("runs", sort_by="host.python_version",
                                         sort_direction="desc"))
    assert len(runs) == 2
    assert runs[0]["host"]["python_version"] == "3.5.2"
    assert runs[1]["host"]["python_version"] == "3.4.3"


filter1 = {"host.os": "Linux", "host.hostname": "ntbacer"}
filter2 = {"result": 2403.52}


@pytest.mark.parametrize("filter", (filter1, filter2))
def test_find_records_filter(mongo_client, filter):
    generic_dao = GenericDAO(mongo_client, "testdb")
    runs = list(generic_dao.find_records("runs", query=filter))
    assert len(runs) == 1
    assert runs[0]["host"]["hostname"] == "ntbacer"
