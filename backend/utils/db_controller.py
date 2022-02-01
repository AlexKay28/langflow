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
from dbase.transitions import TransitionSuccess, TransitionShift

# from utils.comparing import get_phrase_shift_vector

POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


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

        dataframe["id"] = dataframe.reset_index().index + 1

        # create transition shift table
        transition_shift_table = pd.DataFrame()
        # create transition success table
        transition_success_table = pd.DataFrame()

        # restricted number of permutations
        iterators = []
        number_of_connected_phrases = 20
        for d in np.array_split(
            dataframe, dataframe.shape[0] // number_of_connected_phrases
        ):
            iterators.append(itertools.permutations(d.index, 2))

        transition_id = 0
        for idx_from, idx_to in itertools.chain(*iterators):
            if idx_from == idx_to:
                continue

            phrases_from = dataframe.iloc[idx_from]
            phrases_to = dataframe.iloc[idx_to]
            for language in ["english", "russian", "ukrainian", "french"]:
                transition_id += 1
                phrase_from = phrases_from[language]
                phrase_to = phrases_to[language]

                # calculate shift vector = n ^ 2 vecs
                shift_vector = np.array(
                    [0]
                )  # TODO: get_phrase_shift_vector(language, phrase_from, phrase_to)

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

    def update_transitions_global(self):
        """
        Update whole transition success table in db using actions
        table by single apply.
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

    def update_transitions(self, language, uuid):
        """
        Update transitions for specified user
        """

        # select last two user actions
        actions = [
            {"phrase_id": r.phrase_id, "score": r.score}
            for r in db.session.query(
                Action.phrase_id,
                Action.score,
            )
            .filter(Action.uuid == uuid)
            .order_by(desc(Action.action_date))
            .limit(2)
        ]

        if len(actions) < 2:
            return

        # get previous & current question ids, score
        previous_phrase_id = actions[1]["phrase_id"]
        current_phrase_id = actions[0]["phrase_id"]
        transition_score = actions[0]["score"]

        # get existed average success
        n_updates = (
            db.session.query(TransitionSuccess.n_updates)
            .filter(
                and_(
                    TransitionSuccess.language == language,
                    TransitionSuccess.phrase_from == previous_phrase_id,
                    TransitionSuccess.phrase_to == current_phrase_id,
                )
            )
            .scalar()
        )

        if not n_updates:
            # pure phrase pair. no connection
            # nothing top update
            return

        average = (
            db.session.query(TransitionSuccess.average_success)
            .filter(
                and_(
                    TransitionSuccess.language == language,
                    TransitionSuccess.phrase_from == previous_phrase_id,
                    TransitionSuccess.phrase_to == current_phrase_id,
                )
            )
            .scalar()
        )

        # inecrement
        n_updates += 1
        new_average_success = average + (transition_score - average) / n_updates

        # update transition pair by score inecrementally
        db.session.query(TransitionSuccess).filter(
            and_(
                TransitionSuccess.language == language,
                TransitionSuccess.phrase_from == previous_phrase_id,
                TransitionSuccess.phrase_to == current_phrase_id,
            )
        ).update({"average_success": new_average_success})
        db.session.commit()

        return 0
