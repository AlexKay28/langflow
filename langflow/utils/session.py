import os
import fasttext
import numpy as np
import pandas as pd

PATH_TO_DATA = "data/phrases.csv"
PATH_TO_MODELS = "language_models/"


class SessionController:
    """
    Session object which contains session parameters
    for correct question formatting and question selection
    """

    def __init__(self, first_language, second_language, level):
        self.first_language = first_language
        self.second_language = second_language
        self.language_model = fasttext.load_model(
            os.path.join(PATH_TO_MODELS, f"{second_language}5.bin")
        )
        self.level = level
        self.pairs = pd.read_csv(
            PATH_TO_DATA,
            usecols=["level", self.first_language, self.second_language],
        )
        self.pairs = self.pairs[
            self.pairs.level.apply(lambda l: l == level if level > 0 else True)
        ][[self.first_language, self.second_language]].values

        # highly dynamic variables
        self.first_language_phrase = None
        self.second_language_phrase_answer = None

    @property
    def is_new_session(self):
        if not self.first_language_phrase and not self.first_language_phrase:
            return True
        return False

    def get_session_langs_phrases(self):
        return self.first_language_phrase, self.second_language_phrase_answer

    def set_session_langs_phrases(
        self, first_language_phrase, second_language_phrase_answer
    ):
        self.first_language_phrase = first_language_phrase
        self.second_language_phrase_answer = second_language_phrase_answer

    def get_pairs(self):
        return self.pairs
