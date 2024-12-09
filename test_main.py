import os
import pytest
import sqlite3
from src import WeatherDatabaseApi, SQL

@pytest.fixture(scope="function")
def temp_db_environment():
    """
    Creates a temporary database for testing and cleans it up afterward.
    """
    test_db_path = "test_db"
    if not os.path.exists("test_data"):
        os.makedirs("test_data")
    test_db_full_path = os.path.join("test_data", test_db_path)
    yield test_db_full_path
    # Cleanup
    if os.path.exists(f"{test_db_full_path}.db"):
        os.remove(f"{test_db_full_path}.db")
    if os.path.exists("test_data"):
        for root, dirs, files in os.walk("test_data", topdown=False):
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def test_sql_read_sql():
    """
    Test the SQL class's ability to read SQL queries.
    """
    query_template = "SELECT * FROM {table} WHERE city = '{city}';"
    query = SQL.read_sql(query_template, table="CityLocation", city="Miami")
    assert query == "SELECT * FROM CityLocation WHERE city = 'Miami';"

def test_database_connection(temp_db_environment):
    """
    Test that the database connection is successfully established.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=False)
    assert isinstance(db_api._conn, sqlite3.Connection)

def test_create_necessary_tables(temp_db_environment):
    """
    Test that necessary tables are created successfully.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=False)
    db_api.create_necessary_tables()
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    tables = ["CityLocation", "CityInterestingFact"]
    for table in tables:
        result = db_api.get_one_item(query.format(table_name=table))
        assert result is not None

def test_push_csv_to_db(temp_db_environment):
    """
    Test inserting CSV data into a database table.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=False)
    db_api.create_necessary_tables()
    csv_url = WeatherDatabaseApi.necessary_csv_files["CityLocation"]
    db_api.push_csv_to_db(csv_url, "CityLocation", auto_create_table=False, truncate_before_inserting=True)
    query = "SELECT COUNT(*) FROM CityLocation;"
    result = db_api.get_one_item(query)
    assert result[0] > 0  # Ensure rows were inserted

def test_get_active_states(temp_db_environment):
    """
    Test retrieving active states from the CityLocation table.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=True)
    active_states = db_api.get_active_states()

    assert active_states 

def test_get_interesting_fact_for_location(temp_db_environment):
    """
    Test retrieving interesting facts for a specific location.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=True)
    fact = db_api.get_interesting_fact_for_location(25.7839, -80.2102)  # Example coordinates for Miami
    assert isinstance(fact, str)  # Check that a fact string is returned

def test_exit_connection(temp_db_environment):
    """
    Test that the database connection is closed successfully.
    """
    db_api = WeatherDatabaseApi(temp_db_environment, deploy_database=False)
    assert db_api.exit() is True
   