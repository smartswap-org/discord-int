import mysql.connector
from loguru import logger
from datetime import datetime
from src.json.read import get_json_content
from src.json.write import write_json

class DatabaseSQL(object):
    def __init__(self, host, user, password, database):
        """
        Initializes the class with database connection information.

        Parameters:
        - host: The database host.
        - user: The username for the connection.
        - password: The password for the connection.
        - database: The database name.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    def connect(self):
        """
        Establishes a connection to the database using the provided information.
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

def init_database(db_name, db_config_file):
    config = get_json_content(db_config_file)
    if config == -1: 
        write_json(db_config_file, {'host': 'localhost', 'user': 'smartswap', 'pass': 'null'})
        print(f"{'db.json'} has been created.")
        exit()
    return DatabaseSQL(
        config["host"],
        config["user"],
        config["pass"],
        db_name
        )