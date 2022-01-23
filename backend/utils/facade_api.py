import os
import json
import requests


class RL:
    "Reinforcement learning service API."

    def __init__(self):
        self.url = os.environ.get("RL_SERVICE_URL")

    def get_pair(self, level, second_language, uuid):
        """
        Return response with new phrase id.
        """
        endpoint = "/get_pair"
        response = json.loads(
            requests.post(
                self.url + endpoint,
                json={
                    "level": level,
                    "second_language": second_language,
                    "uuid": uuid,
                },
            ).text
        )
        return response


class NLP:
    "Natural language processing service API."

    def __init__(self):
        self.url = os.environ.get("NLP_SERVICE_URL")

    def get_similarity(self, language, phrase1, phrase2):
        """
        Return response with new phrase id.
        """
        endpoint = "/get_similarity"
        response = json.loads(
            requests.get(
                self.url + endpoint,
                json={
                    "language": language,
                    "phrase1": phrase1,
                    "phrase2": phrase2,
                },
            ).text
        )
        print(response)
        return response


class FacadeAPI:
    def __init__(self):
        self.rl_service = RL()
        self.nlp_service = NLP()

    def rl_get_pair(self, level, second_language, uuid):
        return self.rl_service.get_pair(level, second_language, uuid)

    def nlp_get_similarity(self, language, phrase1, phrase2):
        return self.nlp_service.get_similarity(language, phrase1, phrase2)
