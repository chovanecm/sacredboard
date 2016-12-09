import sacredboard.webapp as wa
import pytest


@pytest.mark.parametrize("config_string",
                         ("", "database_name", "789:db_name", "anotherhost:789:db_name", "bla:bla:bla"))
def test_add_mongo_config(config_string):
    app = wa.Flask(__name__)
    if config_string == "bla:bla:bla":
        with pytest.raises(ValueError):
            wa.add_mongo_config(app, config_string)
    else:
        wa.add_mongo_config(app, config_string)
        mongo_client = app.config["data"]
        if config_string == "":
            assert (mongo_client._db_name == "sacred")
            assert (mongo_client._port == 27017)
            assert (mongo_client._host == "localhost")
        elif config_string == "database_name":
            assert (mongo_client._db_name == "database_name")
            assert (mongo_client._port == 27017)
            assert (mongo_client._host == "localhost")
        elif config_string == "789:db_name":
            assert (mongo_client._db_name == "db_name")
            assert (mongo_client._port == 789)
            assert (mongo_client._host == "localhost")
        elif config_string == "anotherhost789:db_name":
            assert (mongo_client._db_name == "db_name")
            assert (mongo_client._port == 789)
            assert (mongo_client._host == "anotherhost")
