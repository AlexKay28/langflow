import os
import numpy as np
import pandas as pd
import itertools

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

        dataframe = dataframe.sample(5)
        dataframe["id"] = dataframe.reset_index().index + 1

        # create transition shift table
        transition_shift_table = pd.DataFrame()
        # create transition success table
        transition_success_table = pd.DataFrame()
        transition_id = 0
        for idx_from, idx_to in itertools.combinations(range(dataframe.shape[0]), 2):
            if idx_from == idx_to:
                continue
            phrases_from = dataframe.iloc[idx_from]
            phrases_to = dataframe.iloc[idx_to]
            for language in ["english", "russian", "ukrainian", "french"]:
                transition_id += 1
                phrase_from = phrases_from[language]
                phrase_to = phrases_to[language]
                shift_vector = get_phrase_shift_vector(language, phrase_from, phrase_to)
                transition_shift_table = transition_shift_table.append(
                    {
                        "language": language,
                        "phrase_from": idx_from + 1,
                        "phrase_to": idx_to + 1,
                        "shift_vector": shift_vector.astype("float16").tolist(),
                    },
                    ignore_index=True,
                )
                transition_success_table = transition_success_table.append(
                    [
                        {
                            "language": language,
                            "user_group": 0,
                            "n_updates": 1,
                            "phrase_from": idx_from + 1,
                            "phrase_to": idx_to + 1,
                            "average_success": 1.0,
                        },
                        {
                            "language": language,
                            "user_group": 0,
                            "n_updates": 1,
                            "phrase_from": idx_to + 1,
                            "phrase_to": idx_from + 1,
                            "average_success": 1.0,
                        },
                    ],
                    ignore_index=True,
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
        transition_shift_table.to_sql(
            "transition_shift",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )
        transition_success_table.to_sql(
            "transition_success",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )

        return 0

    def update_transitions(self):
        """
        Update transition success table in db using actions table.
        """

        # read actions table
        actions_table = pd.read_sql("SELECT * FROM actions", self.dbconnector.engine)

        # read transition success table
        transition_success_table = pd.read_sql(
            "SELECT * FROM transition_success", self.dbconnector.engine
        )

        # inecrementally update transition success table
        for user_id in actions_table["uuid"].unique():
            user_story_subtable = (
                actions_table[actions_table["uuid"] == user_id]
                .reset_index(drop=True)
                .sort_values("action_date")
            )
            if user_story_subtable.shape[0] == 1:
                continue
            for idx in range(1, user_story_subtable.shape[0]):
                previous_step = user_story_subtable.iloc[idx - 1]
                current_step = user_story_subtable.iloc[idx]
                previous_phrase_id = previous_step["phrase_id"]
                current_phrase_id = current_step["phrase_id"]
                transition_score = current_step["score"]
                current_language = current_step["second_language"]

                if current_phrase_id == previous_phrase_id:
                    continue

                # find needed transition index
                needed_index = transition_success_table[
                    (transition_success_table["phrase_from"] == previous_phrase_id)
                    & (transition_success_table["phrase_to"] == current_phrase_id)
                    & (transition_success_table["language"] == current_language)
                ].index[0]

                # read actual values
                n_updates = transition_success_table.loc[needed_index, "n_updates"]
                average = transition_success_table.loc[needed_index, "average_success"]

                # update values inecrementally
                n_updates += 1
                average += (transition_score - average) / n_updates

                # record new values
                transition_success_table.loc[needed_index, "n_updates"] = n_updates
                transition_success_table.loc[needed_index, "average_success"] = average

        transition_success_table = transition_success_table.fillna(0.95)

        # record new transition success matrix
        transition_success_table.to_sql(
            "transition_success",
            self.dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )

        return 0
