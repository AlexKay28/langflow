import os
import numpy as np
import pandas as pd

from sqlalchemy import and_, or_, not_

from dbase import db
from dbase.database_connector import DatabaseConnector
from utils.comparing import get_phrase_shift_vector


class DbController:
    """
    Allows to perform operations with the project database.
    """

    def __init__(self):
        self.dbconnector = DatabaseConnector(
            "langflow", "postgres", 123456, "localhost", 5432
        )

    def upload_phrases_to_db(self, dataframe: pd.DataFrame):
        """
        Upload provided data to database replacing the previous one

        :param dataframe: pandas dataframe to upload to base
        """
        # check needed columns
        assert all(
            [
                col in dataframe.columns
                for col in ["level", "english", "russian", "ukrainian", "french"]
            ]
        )

        # upload data to base
        dataframe.to_sql(
            "phrases",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )

        # create transition shift table
        # TODO: get_phrase_shift_vector

        # create transition success table
        # TODO

        return 0

    def update_transitions(self):
        """
        Update transition success table in db using actions table.
        """

        # read actions table
        # TODO

        # read transition success table
        # TODO

        # inecrementally update transition success table
        # TODO

        # record new transition success matrix
        # TODO

        return 0
