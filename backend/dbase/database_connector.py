import time
import psycopg2
import sqlalchemy
import pandas as pd


class DatabaseConnector:
    """
    Connector to database with interface of interaction activity:
        - upload data to db
        - load data from db
        - update data in db

    :param dbname: the name of the connected database
    :param username: the database user name
    :param password: the database user password
    :param host: the database host name
    :param port: the database port number
    :param conn: database connection object
    :param engine: connection to defined database
    :param cur: cursor to db
    """

    def __init__(self, dbname: str, username: str, password: str, host: str, port: str):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.port = int(port)

        while 1:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                )
                break
            except psycopg2.OperationalError:
                print(f"Retry to connect: {self.dbname}")
                time.sleep(5)
        self.engine = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
        )
        self.cur = self.conn.cursor()

    def __enter__(self):
        """
        Make a database connection and return it
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Make sure the dbconnection gets closed
        """
        self.conn.close()
        self.engine.dispose()
        self.cur.close()
