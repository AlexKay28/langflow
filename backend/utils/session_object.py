import os
import uuid
import numpy as np
import pandas as pd
from collections import Counter
from typing import Tuple
from sqlalchemy import and_, or_, not_

from dbase import db
from dbase.users import UserAuthorized, UserAnon
from dbase.actions import Action
from dbase.phrases import Phrase
from dbase.database_connector import DatabaseConnector

N_MAX_USERS = 25


def generate_random_token(type: str) -> str:
    """
    Generate unique encoded string

    :param type: the encoding type which should be applied

    :return: the generated encoding string
    """
    if type == "uuid4":
        return uuid.uuid4()
    elif type == "os_8":
        return os.urandom(8).hex()
    else:
        raise KeyError(f"Unknown encoding type <{type}>")


class SessionController:
    """
    Session object which contains session parameters
    for correct question formatting and question selection

    :param n_jobs: the number of simultaneously used cores for processing. If the
     value is defined as -1 then all available cpu cores are used.
    """

    def __init__(self, n_jobs: int = -1):
        self.n_jobs = n_jobs

    def is_user(self, uuid: str) -> bool:
        """
        Check particular user existance

        :param uuid: the string with uuid to look for in db

        :return: boolean value was user created or not
        """
        return uuid in self.db.users_uuid_list

    @staticmethod
    def activate_session_token(
        username: str, password: str, is_anon: bool
    ) -> Tuple[str, bool]:
        """
        Activate user session

        :param username: provided username.
        :param password: provided password.
        :param is_anon: is user work as anonimous user or authorized.

        :return: tuple of values - generated token and generation status check (str, bool)
        """

        if is_anon:
            uuid_generated = generate_random_token("uuid4")
            session_token_generated = generate_random_token("os_8")
            user = UserAnon(
                username=username,
                uuid=uuid_generated,
                session_token=session_token_generated,
            )
            db.session.add(user)
            db.session.commit()
        else:
            # TODO
            raise NotImplementedError

        return session_token_generated, True

    @staticmethod
    def get_user_uuid(session_token: str) -> str:
        """
        Get user unique id (uuid) from users table.

        :param session_token: active session token from server side.

        :return: uuid of user from base.
        """
        uuid = (
            db.session.query(UserAnon.uuid)
            .filter(UserAnon.session_token == session_token)
            .scalar()
        )
        return str(uuid)

    @staticmethod
    def get_question_quid(quid_token: str) -> str:
        """
        Get user unique id (uuid) from users table.

        :param quid_token: the question token server side

        :return: quid from base
        """
        quid = (
            db.session.query(Action.quid)
            .filter(Action.quid_token == quid_token)
            .scalar()
        )
        return str(quid)

    @staticmethod
    def select_question(
        uuid: str, first_language: str, second_language: str, level: int
    ) -> Tuple[str, str, str]:
        """
        Smart question selection

        :param uuid: the uuid of user which asks to get the question
        :param first_language: the language which is known by user
        :param second_language: the language which is learning by user
        :param level: the level which defined the hardness of the asked phrase

        :return: tuple which consts of question id, and phrase on two languages
        """

        if level > 0:
            phrases_id = (
                db.session.query(Phrase.id).filter(Phrase.level == level).distinct()
            )
        else:
            phrases_id = db.session.query(Phrase.id).distinct()

        # normalize pair
        phrase_id = int(np.random.choice([r.id for r in phrases_id]))

        flang = str(
            db.session.query(getattr(Phrase, first_language))
            .filter(Phrase.id == phrase_id)
            .scalar()
        )
        slang = str(
            db.session.query(getattr(Phrase, second_language))
            .filter(Phrase.id == phrase_id)
            .scalar()
        )

        flang, slang = flang.lower().capitalize(), slang.lower().capitalize()
        return phrase_id, flang, slang

    def generate_phrase_pair(
        self, uuid: str, first_language: str, second_language: str, level: int
    ) -> Tuple[str, str]:
        """
        Choose pair of phrases randomly

        :param uuid: the uuid of user which asks to get the question
        :param first_language: the language which is known by user
        :param second_language: the language which is learning by user
        :param level: the level which defined the hardness of the asked phrase

        :return: the tuple of three values with question id and phrase on two languages
        """
        # smart selection
        phrase_id, flang, slang = self.select_question(
            uuid, first_language, second_language, level
        )

        # generate question id and token
        quid_generated = generate_random_token("uuid4")
        quid_token_generated = generate_random_token("os_8")

        # record action in base
        action = Action(
            uuid=uuid,
            quid=quid_generated,
            quid_token=quid_token_generated,
            phrase_id=phrase_id,
            level=level,
            first_language=first_language,
            second_language=second_language,
            user_answer=None,
            score=None,
        )
        db.session.add(action)
        db.session.commit()

        return quid_token_generated, flang, slang

    def get_user_phrases(self, uuid: str, quid: str) -> Tuple[str, str, str, str]:
        """
        Get particular question of particular user

        :param uuid: the user id for existed pair selection
        :param quid: the question id for existed pair selection

        :return: the tuple of four values with languages names and phrase on both of themh
        """

        row = (
            db.session.query(Action)
            .filter(and_(Action.quid == quid, Action.uuid == uuid))
            .scalar()
        )
        phrase_id = row.phrase_id
        flang = row.first_language
        slang = row.second_language

        phrases = db.session.query(Phrase).filter(Phrase.id == phrase_id).scalar()
        flang_phrase = getattr(phrases, flang)
        slang_phrase = getattr(phrases, slang)

        return flang, flang_phrase, slang, slang_phrase

    def record_users_result(self, uuid: str, quid: str, user_answer: str, score: float):
        """
        Set question status of user

        :param uuid: the user id to record in the table of actions
        :param quid: the question id to record in the table of actions
        :param user_answer: the user answer to record in the table of action
        :param score: the user's answer score to record in the table of actions
        """
        db.session.query(Action).filter(
            and_(Action.quid == quid, Action.uuid == uuid)
        ).update({"user_answer": user_answer, "score": round(score, 3)})
        db.session.commit()

    def get_user_analysis(self, uuid: str) -> dict:
        """
        Get user's session analysis

        :param uuid: the user id to analyze

        :return: dictionary of the main info about user's success
        """
        # retrieve info from base
        actions = [
            {"second_language": r.second_language, "score": r.score}
            for r in db.session.query(
                Action.second_language,
                Action.score,
            ).filter(Action.uuid == uuid)
        ]
        slangs = [a["second_language"] for a in actions]
        scores = [a["score"] for a in actions]

        # count target values frequency
        slangs_counts = dict(Counter(slangs))

        # collect stats how user successfully stidy
        answered_questions = [s for s in scores if s is not None]
        answered_questions_number = len(answered_questions)
        unanswered_questions_number = len(scores) - len(answered_questions)
        average_score = np.mean(answered_questions)
        message = "Study more, lazy boy!"

        return (
            slangs_counts,
            answered_questions,
            answered_questions_number,
            unanswered_questions_number,
            average_score,
            message,
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
        dbconnector = DatabaseConnector(
            "langflow", "postgres", 123456, "localhost", 5432
        )
        df.to_sql(
            "phrases",
            dbconnector.engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi",
        )
        return 0
