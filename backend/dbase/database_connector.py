import psycopg2
import sqlalchemy
import pandas as pd


class DatabaseConnector:
    """
    Connector to database with interface of interaction activity:
        - upload data to db
        - load data from db
        - update data in db

    :param conn: database connection object
    :param engine: connection to defined database
    :param cur: cursor to db
    """

    def __init__(self, dbname, username, password, host, port):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )
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
