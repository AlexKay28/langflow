import os
import uuid
import numpy as np
import pandas as pd

from typing import Tuple

from utils.user import User
from utils.storage import StorageDB

from dbase import db
from dbase.users import UserAuthorized, UserAnon

N_MAX_USERS = 25


class SessionController:
    """
    Session object which contains session parameters
    for correct question formatting and question selection
    """

    def __init__(self):
        # data and users database
        self.db = StorageDB()

    def is_user(self, uuid: str):
        """
        Check particular user existance
        """
        return uuid in self.db.users_uuid_list

    def activate_session_token(
        self, username: str, password: str, is_anon: bool
    ) -> Tuple[str, bool]:
        """
        Activate user session
        """

        if is_anon:
            uuid_generated = uuid.uuid4()
            session_token_generated = uuid.uuid4()
            u = UserAnon(
                username=username,
                uuid=uuid_generated,
                session_token=session_token_generated,
            )
            db.session.add(u)
            db.session.commit()
        else:
            # TODO
            raise NotImplementedError

        return session_token_generated, self.is_user(uuid_generated)

    def generate_phrase_pair(
        self, uuid: str, first_language: str, second_language: str, level: int
    ) -> Tuple[str, str]:
        """
        Choose pair of phrases randomly
        """
        user = self.db.get_user(uuid)

        user.first_language = first_language
        user.second_language = second_language
        user.level = level

        pairs = self.db.get_pairs()
        quid, first_lang, second_lang = user.generate_question(pairs)
        return quid, first_lang, second_lang

    def get_user_phrases(self, uuid: str, quid: str):
        """
        Get particular question of particular user
        """
        user = self.db.get_user(uuid)
        question_entity = user.get_question(quid)
        return (
            question_entity["first_language"],
            question_entity["first_language_phrase"],
            question_entity["second_language"],
            question_entity["second_language_phrase_answer"],
        )

    def record_users_result(self, uuid: str, quid: str, equality_rate: float):
        """
        Set question status of user
        """
        user = self.db.get_user(uuid)
        user.set_answer_status(quid, equality_rate)

    def get_user_analysis(self, uuid: str):
        """
        Get user's session analysis
        """
        user = self.db.get_user(uuid)
        return {
            "uuid": uuid,
            "statistics": user.get_user_statistics(),
        }
