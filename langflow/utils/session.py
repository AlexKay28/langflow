import os
import gzip
import shutil
import fasttext
import numpy as np
import pandas as pd

PATH_TO_DATA = "data/phrases.csv"
PATH_TO_MODELS = "language_models/"


def extract_language_models(model_name, extension=".gz"):
    """
    Models are stored as .bit.tar.gz
    Fore session working they are needed to be extracted
    """
    archive_path = os.path.join(PATH_TO_MODELS, f"{model_name}.gz")
    model_path = os.path.join(PATH_TO_MODELS, f"{model_name}")

    if model_name in os.listdir(PATH_TO_MODELS):
        return

    with gzip.open(archive_path, "rb") as file_in:
        with open(model_path, "wb") as file_out:
            shutil.copyfileobj(file_in, file_out)


class SessionController:
    """
    Session object which contains session parameters
    for correct question formatting and question selection
    """

    def __init__(self, first_language, second_language, level):
        self.first_language = first_language
        self.second_language = second_language
        self.level = level
        self.pairs = pd.read_csv(
            PATH_TO_DATA,
            usecols=["level", self.first_language, self.second_language],
        )
        self.pairs = self.pairs[
            self.pairs.level.apply(lambda l: l == level if level > 0 else True)
        ][[self.first_language, self.second_language]].values

        self.model_name = f"{second_language}5.bin"
        extract_language_models(self.model_name)
        self.language_model = fasttext.load_model(
            os.path.join(PATH_TO_MODELS, self.model_name)
        )

        # highly dynamic variable
        self.questions_query = {}

    @property
    def is_new_session(self):
        if questions_query:
            return False
        return True

    def get_session_langs_phrases(self, uuid: str):
        return (
            self.questions_query[uuid]["first_language_phrase"],
            self.questions_query[uuid]["second_language_phrase_answer"],
        )

    def set_session_langs_phrases(
        self,
        uuid: str,
        first_language_phrase: str,
        second_language_phrase_answer: str,
    ):
        self.questions_query[uuid] = {
            "first_language_phrase": first_language_phrase,
            "second_language_phrase_answer": second_language_phrase_answer,
        }

    def reset_session(self):
        self.questions_query = {}

    def get_pairs(self):
        return self.pairs
