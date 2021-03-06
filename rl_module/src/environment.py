import os
import numpy as np
import pandas as pd
from typing import Tuple

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
    Observation:
        Type:
        Num     Observation                   Representation
        0       The shift vector till
                the first closest question    (phrase_id, prob)
        1       The shift vector till
                the second closest question   (phrase_id, prob)
        2       The shift vector till
                the third closest question    (phrase_id, prob)
    Actions:
        Type: Discrete(2)
        Num   Action
        0     Choose the first closest question
        1     Choose the second closest question
        2     Choose the third closest question
    Reward:
        Reward is between [0, 1] and estimated by semantic closeness
    Starting State:
        Randomly
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

        self.transition_success_table = pd.read_sql(
            f"SELECT * FROM transition_success", self.db.engine
        )
        self.n_questions_to_consider = 5

    def get_user_state(self, uuid):
        """
        Find previous user state and select all possible states with their success probs.

        :param uuid: user id

        :return: list of probs for each next phrase and id of phrase.
                 [(phrase_id1, prob1), (phrase_id2, prob2)]
        """
        n_previous = 15

        query = (
            f"SELECT * FROM actions WHERE uuid = '{uuid}' "
            f"ORDER BY action_date DESC LIMIT {n_previous}"
        )
        user_actions_table = pd.read_sql(query, self.db.engine)

        relevant_table = self.transition_success_table

        # n_user_actions = user_actions_table.shape[0]
        # if n_user_actions > 0:
        #     last_phrase_id = user_actions_table["phrase_id"].iloc[0]
        #     # TODO: build connections between chunks
        #     relevant_table = self.transition_success_table[
        #         self.transition_success_table.phrase_from == last_phrase_id
        #     ]

        possible_states_phrases = relevant_table["phrase_to"].to_list()
        possible_states_probs = relevant_table["average_success"].to_list()

        state = [
            (phrase, 1 - prob)
            for phrase, prob in zip(possible_states_phrases, possible_states_probs)
        ]

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
