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
from dbase.phrases import Phrase, update_data_csv

N_MAX_USERS = 25


def generate_random_token(type):
    """
    Generate unique encoded string
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
    """

    def __init__(self):
        pass

    def is_user(self, uuid: str):
        """
        Check particular user existance
        """
        return uuid in self.db.users_uuid_list

    @staticmethod
    def activate_session_token(
        username: str, password: str, is_anon: bool
    ) -> Tuple[str, bool]:
        """
        Activate user session
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
    def get_user_uuid(session_token):
        """
        Get user unique id (uuid) from users table.
        """
        uuid = (
            db.session.query(UserAnon.uuid)
            .filter(UserAnon.session_token == session_token)
            .scalar()
        )
        return str(uuid)

    @staticmethod
    def get_question_quid(quid_token):
        """
        Get user unique id (uuid) from users table.
        """
        quid = (
            db.session.query(Action.quid)
            .filter(Action.quid_token == quid_token)
            .scalar()
        )
        return str(quid)

    @staticmethod
    def select_question(uuid, first_language, second_language, level):
        """
        Smart question selection
        """
        # table_df = pd.read_csv("tmp/phrases.csv")
        # table_df["level"] = table_df["level"].astype("int")
        # update_data_csv(table_df)

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

    def get_user_phrases(self, uuid: str, quid: str):
        """
        Get particular question of particular user
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
        """
        db.session.query(Action).filter(
            and_(Action.quid == quid, Action.uuid == uuid)
        ).update({"user_answer": user_answer, "score": round(score, 3)})
        db.session.commit()

    def get_user_analysis(self, uuid: str):
        """
        Get user's session analysis
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

        return {
            "target_languages_counts": slangs_counts,
            "answered_questions_number": answered_questions_number,
            "unanswered_questions_number": unanswered_questions_number,
            "average_score": average_score,
            "Inference": "Study more, lazy boy!",
        }
