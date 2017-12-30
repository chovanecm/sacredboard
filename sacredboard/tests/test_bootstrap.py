# coding=utf-8
import pytest

import sacredboard.bootstrap as bootstrap


@pytest.fixture
def app():
    return bootstrap.Flask(__name__)


@pytest.fixture()
def app_config():
    return {
        "http.serve_on_endpoint": "/",
        "http.port": 5000,
        "debug": False
    }

@pytest.mark.parametrize("config_string",
                         ("", "database_name", "789:db_name",
                          "anotherhost:789:db_name", "bla:bla:bla"))
def test_add_mongo_config(config_string, app):
    if config_string == "bla:bla:bla":
        with pytest.raises(ValueError):
            bootstrap.add_mongo_config_simple(app, config_string, "collection_name")
    else:
        bootstrap.add_mongo_config_simple(app, config_string, "collection_name")
        mongo_client = app.config["data"]
        if config_string == "":
            assert mongo_client._uri == "mongodb://localhost:27017"
            assert (mongo_client._db_name == "sacred")
        elif config_string == "database_name":
            assert mongo_client._uri == "mongodb://localhost:27017"
            assert (mongo_client._db_name == "database_name")
        elif config_string == "789:db_name":
            assert mongo_client._uri == "mongodb://localhost:789"
            assert (mongo_client._db_name == "db_name")
        elif config_string == "anotherhost:789:db_name":
            assert mongo_client._uri == "mongodb://anotherhost:789"
            assert (mongo_client._db_name == "db_name")


@pytest.mark.parametrize("connection_string", ("mongodb://user:password@192.168.0.1:1234?connectTimeoutMS=300000",
                                               "mongodb://192.168.0.1:1234?connectTimeoutMS=300000"))
def test_add_mongo_config_with_uri(connection_string, app):
    bootstrap.add_mongo_config_with_uri(app, connection_string, "db_name", "collection_name")
    mongo_client = app.config["data"]

    if connection_string == "mongodb://user:password@192.168.0.1:1234?connectTimeoutMS=300000":
        assert mongo_client._uri == "mongodb://user:password@192.168.0.1:1234?connectTimeoutMS=300000"
    elif connection_string == "mongodb://192.168.0.1:1234?connectTimeoutMS=300000":
        assert mongo_client._uri == "mongodb://192.168.0.1:1234?connectTimeoutMS=300000"

    assert (mongo_client._db_name == "db_name")


def test_module_initialisation_method_call_only(app_config):
    """Only test calling module initialisation to see that no module causes the application to crash"""
    bootstrap._initialize_modules(app_config)
