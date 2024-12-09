import sqlite3
import csv
import urllib.request
import logging


logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose logging
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)


class SQL:
    @classmethod
    def read_sql(cls, query, **params):
        if query.strip().endswith(".sql"):
            with open(query, "r") as file:
                query = file.read().strip()

        return query.format(**params)


class WeatherDatabaseApi:

    necessary_csv_files = {
        "CityLocation": "https://raw.githubusercontent.com/Cavidan-oss/IDS_706_Final_Project/refs/heads/main/data/csv/processed/uscities_processed.csv",
        "CityInterestingFact": "https://raw.githubusercontent.com/Cavidan-oss/IDS_706_Final_Project/refs/heads/main/data/csv/raw/city_facts.csv",
    }

    def __init__(self, database_connection_string, deploy_database=False) -> None:
        logging.info("Initializing WeatherDatabaseApi class.")
        self.database_connection_string = database_connection_string
        self.deploy_database = deploy_database

        self._conn = self.connect_to_db(self.database_connection_string)

        if self.deploy_database:
            logging.info("Deploying the database.")
            db_status = self.check_database_deployment()

            if not db_status:
                logging.info("Database not fully deployed. Creating necessary tables.")
                self.create_necessary_tables()

                for (
                    table_name,
                    csv_path,
                ) in WeatherDatabaseApi.necessary_csv_files.items():
                    self.push_csv_to_db(
                        csv_path, table_name, truncate_before_inserting=True
                    )

    def connect_to_db(self, database_connection_string):
        try:
            conn = sqlite3.connect(f"{database_connection_string}.db")
            logging.info(f"Connected to database: {database_connection_string}")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to database: {e}")
            raise

    def get_connection(self):
        if not self._conn:
            logging.error("Connection with database failed! Attempting to reconnect.")
            raise Exception("Connection with database failed! Try reconnecting.")

        return self._conn

    def execute_query(self, query):
        connection = self.get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            logging.info(f"Query executed successfully: {query}")
            cursor.close()
            return True
        except Exception as e:
            logging.error(f"Error executing query: {query} | Error: {e}")
            return False

    def get_item(self, query, cursor):
        logging.debug(f"Executing iterator query: {query}")
        cursor.execute(query)
        for result in cursor.fetchall():
            yield result

    def get_one_item(self, query):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            logging.debug(f"Executing query to fetch one item: {query}")
            for item in self.get_item(query, cursor):
                return item
        except Exception as e:
            logging.error(f"Error fetching item: {e}")
            raise e

    def get_all_item(self, query):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            logging.debug(f"Executing query to fetch all items: {query}")
            items = [item for item in self.get_item(query, cursor)]
            return items
        except Exception as e:
            logging.error(f"Error fetching all items: {e}")
            raise e

    def create_necessary_tables(self):
        create_table = """
            CREATE TABLE IF NOT EXISTS CityLocation (
                row_id INTEGER PRIMARY KEY,
                city TEXT,
                city_ascii TEXT,
                state_id TEXT,
                state_name TEXT,
                county_fips INTEGER,
                county_name TEXT,
                lat REAL,
                lng REAL,
                population INTEGER,
                density INTEGER,
                source TEXT,
                military BOOLEAN,
                incorporated BOOLEAN,
                timezone TEXT,
                ranking INTEGER,
                zips TEXT,
                id INTEGER,
                active_cities INTEGER
            );  
        """

        create_table2 = """
            CREATE TABLE IF NOT EXISTS CityInterestingFact (
                id INTEGER PRIMARY KEY,
                city TEXT,
                state_name TEXT,
                fact TEXT
            );
        """

        self.execute_query(create_table)
        self.execute_query(create_table2)

        logging.info("Necessary tables created successfully.")

        return True

    def check_database_deployment(self):
        sqllite_check_table = (
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        )

        self.needed_table_names = list(WeatherDatabaseApi.necessary_csv_files.keys())
        res_list = []

        for table in self.needed_table_names:
            res = self.get_one_item(sqllite_check_table.format(table_name=table))
            res_list.append(bool(res))

        logging.info(
            f"Database deployment status: {'Deployed' if all(res_list) else 'Not Deployed'}"
        )
        return all(res_list)

    def push_csv_to_db(
        self,
        csv_file_path,
        table_name,
        auto_create_table=False,
        truncate_before_inserting=False,
    ):
        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            if csv_file_path.startswith("http"):
                response = urllib.request.urlopen(csv_file_path)
                lines = [l.decode("utf-8") for l in response.readlines()]
                csv_reader = csv.reader(lines)
            else:
                with open(
                    csv_file_path, mode="r", newline="", encoding="utf-8"
                ) as csvfile:
                    csv_reader = csv.reader(csvfile)

            header = next(csv_reader)
            placeholders = ", ".join(["?" for _ in header])

            if auto_create_table:
                columns_to_create_table = ", ".join(
                    [
                        f"{col.replace('.', '_').replace(' ', '_')} TEXT"
                        for col in header
                    ]
                )
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_to_create_table})"
                )

            if truncate_before_inserting:
                cursor.execute(f"DELETE FROM {table_name}")

            sql_insert = f"INSERT INTO {table_name} VALUES ({placeholders})"

            for row in csv_reader:
                cursor.execute(sql_insert, row)

            connection.commit()
            logging.info(f"Data from {csv_file_path} inserted into table {table_name}.")
            return True
        except Exception as e:
            logging.error(f"Error inserting CSV data into table {table_name}: {e}")
            raise e

    def get_active_states(self):
        query = "SELECT lat, lng, state_name, city FROM CityLocation WHERE active_cities = 1;"
        raw_res = self.get_all_item(query)

        res = {(row[0], row[1]): {"state": row[2], "city": row[3]} for row in raw_res}
        logging.debug(f"Active states retrieved: {res}")
        return res

    def get_interesting_fact_for_location(self, lat, long, randomize=True):
        query = """
            SELECT cif.fact FROM CityInterestingFact cif
            LEFT JOIN CityLocation cl ON cif.city = cl.city AND cl.state_name = cif.state_name
            WHERE lat = {lat} AND lng = {long} 
        """

        raw_res = self.get_one_item(query.format(lat=lat, long=long))
        logging.debug(f"Interesting fact for location ({lat}, {long}): {raw_res}")
        return raw_res[0]

    def exit(self):
        current_conn = self.get_connection()
        if current_conn:
            current_conn.close()
            logging.info("Database connection closed.")
        return True


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    test_connection = WeatherDatabaseApi("data/db/application", deploy_database=True)
    test_connection.execute_query(
        """UPDATE CityLocation SET active_cities = 1 WHERE city = 'Miami' and state_name = 'Florida'"""
    )
    # res = test_connection.get_interesting_fact_for_location( 40.6943,  -73.9249)

    # print(res)
    # test_connection.push_csv_to_db(WeatherDatabaseApi.necessary_csv_files.get('CityLocation'), 'CityLocation', True, True)

    # query = "SELECT lat, lng, state_name, city FROM CityLocation WHERE active_cities = 1;"

    # # res = test_connection.get_all_item(query)
    # res = test_connection.get_active_states()
    # print(res)
    # test_connection.exit()
