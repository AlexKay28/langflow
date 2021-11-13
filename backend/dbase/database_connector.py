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

    def __init__(self, dbname: str, username: str, password: str, host: str, port: int):
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

    def upload_df_table(
        self, df: pd.DataFrame, schema: str, table_name: str, if_exists: str = "fail"
    ):
        """
        Upload pd.DataFrame table to SQL database

        :param df: dataframe which is needed to be loaded
        :param schema: database schema
        :param table_name: name if the table in base
        :param if_exists: How to behave if the table already exists
         available values {‘fail’, ‘replace’, ‘append’}
        """
        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            method="multi",
        )
