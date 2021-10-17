import os
import uuid
import gzip
import shutil
import fasttext
import numpy as np
import pandas as pd

from typing import Tuple

from utils.user import User
from utils.storage import StorageDB

N_MAX_USERS = 25
PATH_TO_MODELS = "language_models/"
AVAILABLE_MODELS = ["english", "french"]  # , "ukrainian", "russian"]


def load_language_models(extension="gz"):
    """
    Models are stored as .bit.tar.gz
    Fore session working they are needed to be extracted
    """
    models = {}
    for model_name in AVAILABLE_MODELS:
        model_name_ext = f"{model_name}5.bin"
        archive_path = os.path.join(PATH_TO_MODELS, f"{model_name_ext}.{extension}")
        model_path = os.path.join(PATH_TO_MODELS, f"{model_name_ext}")

        if model_name_ext not in os.listdir(PATH_TO_MODELS):
            with gzip.open(archive_path, "rb") as file_in:
                with open(model_path, "wb") as file_out:
                    shutil.copyfileobj(file_in, file_out)

        models[model_name] = fasttext.load_model(model_path)

    return models


class SessionController:
    """
    Session object which contains session parameters
    for correct question formatting and question selection
    """

    def __init__(self):
        # init models
        self.language_models = load_language_models()

        # data and users database
        self.db = StorageDB()

    def is_user(self, uuid: str):
        """
        Check particular user existance
        """
        return uuid in self.db.users_uuid_list

    def create_user(
        self, first_language: str, second_language: str, level: int
    ) -> Tuple[str, bool]:
        """
        Create user object and add it in self.users class attribute
        """
        if len(self.db.users_uuid_list) > N_MAX_USERS:
            self.db.reset_users()
        uuid_generated = str(uuid.uuid4())
        user = User(uuid_generated, first_language, second_language, level)
        self.db.add_user(uuid_generated, user)
        return uuid_generated, self.is_user(uuid_generated)

    def generate_phrase_pair(self, uuid: str) -> Tuple[str, str]:
        """
        Choose pair of phrases randomly
        """
        user = self.db.get_user(uuid)
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
            question_entity["first_language_phrase"],
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
