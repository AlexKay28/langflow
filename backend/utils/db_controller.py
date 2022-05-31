import os
import sys
import numpy as np
import pandas as pd
import itertools

from sqlalchemy import and_, or_, not_
from sqlalchemy import desc

from dbase import db
from dbase.database_connector import DatabaseConnector
from dbase.actions import Action

from utils.helpers import get_phrase_links
from utils.facade_api import FacadeAPI

# set other services connection
NLP_SERVICE_URL = os.environ.get("NLP_SERVICE_URL")
facade_api = FacadeAPI(
    nlp_url=NLP_SERVICE_URL,
)


POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

_TRANSITIONS_NEIGHBOURS = 10


class DbController:
    """
    Allows to perform operations with the project database.
    """

    def __init__(self):
        self.dbconnector = DatabaseConnector(
            POSTGRES_NAME,
            POSTGRES_USERNAME,
            POSTGRES_PASSWORD,
            POSTGRES_HOST,
            POSTGRES_PORT,
        )

    def upload_phrases_to_db(self, dataframe: pd.DataFrame):
        """
        Upload provided data to database replacing the previous one.
        Methods uploads phrases to database, transition shift vector and
        transition success matrices.

        :param dataframe: pandas dataframe to upload to base
        """
        # check needed columns
        assert all(
            [
                col in dataframe.columns
                for col in ["level", "english", "russian", "ukrainian", "french"]
            ]
        )

        # add index column for query adressing
        dataframe["id"] = dataframe.reset_index().index + 1

        # get vectors
        phrase_vectors = dataframe[["id"]]
        for language in ["english", "russian", "ukrainian", "french"]:
            phrase_vectors[language] = dataframe[language].apply(
                lambda phrase: facade_api.nlp_get_phrase_vector(language, phrase)[
                    "vector"
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
        phrase_vectors.to_sql(
            "phrases_vecs",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )

        return 0
