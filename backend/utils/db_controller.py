import os
import sys
import numpy as np
import pandas as pd
import itertools

from sqlalchemy import and_, or_, not_
from sqlalchemy import desc

from dbase import db
from dbase.database_connector import DatabaseConnector
from dbase.phrases import Phrase, PhraseVector

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

    def upload_phrases_to_db(self, phrases: pd.DataFrame):
        """
        Upload provided data to database replacing the previous one.
        Methods uploads phrases to database, transition shift vector and
        transition success matrices.

        :param phrases: pandas dataframe to upload to base
        """
        # check needed columns
        assert all(
            [
                col in phrases.columns
                for col in ["level", "english", "russian", "ukrainian", "french"]
            ]
        )

        # add index column for query adressing
        phrases["id"] = phrases.reset_index()["index"] + 1

        # upload data to base
        phrases.to_sql(
            "phrases",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )

        # get vectors
        phrases_vec = phrases[["id"]]
        for language in ["english", "russian", "ukrainian", "french"]:
            phrases_vec[language] = phrases[language].apply(
                lambda phrase: facade_api.nlp_get_phrase_vector(language, phrase)[
                    "vector"
                ]
            )

        # delete all the records in the existed table
        db.session.query(PhraseVector).delete()
        db.session.commit()

        for index, row in phrases_vec.iterrows():
            phrase_vec = PhraseVector(
                id=row["id"],
                english=row["english"],
                french=row["french"],
                russian=row["russian"],
                ukrainian=row["ukrainian"],
            )
            db.session.add(phrase_vec)
            db.session.commit()
