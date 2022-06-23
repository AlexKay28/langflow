import os
import ast
import numpy as np
import pandas as pd
from typing import Tuple

from sklearn.neighbors import NearestNeighbors

from src.database_connector import DatabaseConnector

POSTGRES_NAME = os.getenv('POSTGRES_NAME', "langflow")
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME', "postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', "123456")
POSTGRES_HOST = os.getenv('POSTGRES_HOST', "localhost")
POSTGRES_PORT = os.getenv('POSTGRES_PORT', "5432")


class QuestionSpaceEnv:
    """
    Description:
        Question space contains phrases ids and their expected probs.
    Reward:
        Reward is between [0, 1] and estimated by semantic closeness
    Episode Termination:
        Defined number of iteration and early stopped
    """

    def __init__(self):
        self.db = DatabaseConnector(
            POSTGRES_NAME,
            POSTGRES_USERNAME,
            POSTGRES_PASSWORD,
            POSTGRES_HOST,
            POSTGRES_PORT,
        )

        phrase_vec_query = f"SELECT * FROM phrases_vecs"
        self.phrase_vec = pd.read_sql(phrase_vec_query, self.db.engine)

        self.knn_model = {}
        for lang in ["russian", "english", "french", "ukrainian"]:
            space = np.array(
                [list(ast.literal_eval(v)) for v in self.phrase_vec[lang].values]
            )
            model = NearestNeighbors(n_neighbors=15, algorithm='auto')
            model.fit(space)
            self.knn_model[lang] = model

    def get_user_state(
        self, uuid: str, second_language: str, n_neighbors: int = 5
    ) -> dict:
        """
        Find previous user state and select all possible states with their success probs.

        :param uuid: user id
        :param second_language: language to calculate
        :param n_neighbors: number of neighbors to select
        :return: user state dict
        """
        user_vec_query = f"SELECT * FROM user_vectors WHERE uuid = '{uuid}'"
        user_vec = pd.read_sql(user_vec_query, self.db.engine)

        vector = user_vec[second_language].to_numpy()[0]

        dists, idxs = self.knn_model[second_language].kneighbors(
            [vector], n_neighbors, return_distance=True
        )
        dists, idxs = dists[0], idxs[0]

        phrase_idx = self.phrase_vec["id"].iloc[idxs]
        phrase_vec = self.phrase_vec[second_language].iloc[idxs]

        state = {
            "user": user_vec,
            "idx": phrase_idx,
            "phrases": phrase_vec,
            "distances": dists,
        }
        return state

    def step(self, action: int) -> Tuple[list, float, bool, dict]:
        """
        Perform a transition step among the questions

        :param action: Chosed transition from the agent's action space.

        :return: The tuple with parameters -
                 next state, reward, transition success status (done), transition info.
        """
        phrase_id, reward, done, info = action, None, None, None
        return action

    def reset(self, seed: int = None):
        """
        Reset state setting a new one randomly

        :param seed: The random seed for state generation.

        :return: the vector of the question state.
        """
        # TODO
