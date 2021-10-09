import os
import gzip
import shutil
import fasttext
import numpy as np
import pandas as pd

from typing import Tuple

from utils.user import User

N_MAX_USERS = 25
PATH_TO_DATA = "data/phrases.csv"
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
        # load application data
        self.pairs = pd.read_csv(PATH_TO_DATA)

        # init models
        self.language_models = load_language_models()

        # highly dynamic variable
        self.users = {}

    def reset_session(self):
        self.users = {}

    def get_pairs(self):
        return self.pairs

    def is_user(self, uuid):
        return uuid in self.users.keys()

    def create_user(
        self, uuid: str, first_language: str, second_language: str, level: int
    ) -> Tuple[str, bool]:
        if len(self.users) > N_MAX_USERS:
            self.reset_session()
        self.users[uuid] = User(uuid, first_language, second_language, level)
        return uuid, self.is_user(uuid)

    def generate_phrase_pair(self, uuid) -> Tuple[str, str]:
        """
        Choose pair of phrases randomly
        """
        quid, flang, slang = self.users[uuid].generate_question(self.pairs)
        return quid, flang, slang

    def get_user_phrases(self, uuid: str, quid: str):
        question_entity = self.users[uuid].get_question(quid)
        return (
            question_entity["first_language_phrase"],
            question_entity["second_language_phrase_answer"],
        )

    def record_users_result(self, uuid: str, quid: str, equality_rate: float):
        self.users[uuid].set_answer_status(quid, equality_rate)

    def get_user_analysis(self, uuid: str):
        return {
            "uuid": uuid,
            "statistics": self.users[uuid].get_user_statistics(),
        }
