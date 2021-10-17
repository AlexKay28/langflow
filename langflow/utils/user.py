import uuid
import numpy as np


class User:
    def __init__(self, uuid, first_language, second_language, level):
        self.uuid = uuid
        self.first_language = first_language
        self.second_language = second_language
        self.level = level

        self.questions = {}

    def generate_question(self, pairs):
        """
        Create question in users metadata
        """
        quid_generated = str(uuid.uuid4())
        pairs = pairs[
            pairs.level.apply(lambda l: l == self.level if self.level > 0 else True)
        ][[self.first_language, self.second_language]].values
        flang, slang = pairs[np.random.choice(len(pairs))]
        flang, slang = flang.lower().capitalize(), slang.lower().capitalize()
        self.questions[quid_generated] = {
            "first_language": self.first_language,
            "first_language_phrase": flang.lower().capitalize(),
            "second_language": self.second_language,
            "second_language_phrase_answer": slang.lower().capitalize(),
        }
        return quid_generated, flang, slang

    def get_question(self, quid):
        """
        Get particular question by quid
        """
        return self.questions[quid]

    def set_answer_status(self, quid, equality_rate):
        """
        Add status of answered question
        """
        self.questions[quid]["status"] = equality_rate

    def get_user_statistics(self):
        """
        Final statistics about users progress while session
        """
        return "User is the great student!"
