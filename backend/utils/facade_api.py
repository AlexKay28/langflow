import os
import json
import requests

from typing import Tuple, Dict


class RL:
    "Reinforcement learning service API."

    def __init__(self, service_url: str):
        self.url = service_url

    def get_pair(self, level: int, second_language: str, uuid: str) -> Dict:
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
        if response["status"] == 200:
            return {"phrase_id": response["phrase_id"]}

        raise Exception(response["traceback"])


class NLP:
    "Natural language processing service API."

    def __init__(self, service_url: str):
        self.url = service_url

    def get_similarity(self, language: str, phrase1: str, phrase2: str) -> Dict:
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
        if response["status"] == 200:
            return {
                "is_equal": response["is_equal"],
                "equality_rate": response["equality_rate"],
                "differences": response["differences"],
            }

        raise Exception(response["traceback"])

    def get_phrase_vector(self, language: str, phrase: str) -> Dict:
        """
        Return response with new phrase id.
        """
        endpoint = "/get_phrase_vector"
        response = json.loads(
            requests.get(
                self.url + endpoint,
                json={
                    "language": language,
                    "phrase": phrase,
                },
            ).text
        )
        vector = [float(f) for f in response["vector"][1:-1].split()]
        if response["status"] == 200:
            return {"vector": vector}

        raise Exception(response["traceback"])


class FacadeAPI:
    def __init__(self, rl_url: str = None, nlp_url: str = None):
        self.rl_service = RL(rl_url)
        self.nlp_service = NLP(nlp_url)

    def rl_get_pair(self, level: int, second_language: str, uuid: str) -> Dict:
        return self.rl_service.get_pair(level, second_language, uuid)

    def nlp_get_similarity(self, language: str, phrase1: str, phrase2: str) -> Dict:
        return self.nlp_service.get_similarity(language, phrase1, phrase2)

    def nlp_get_phrase_vector(self, language: str, phrase: str) -> Dict:
        return self.nlp_service.get_phrase_vector(language, phrase)
