import numpy as np
from typing import Tuple


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

    def __init__(self, db):
        self.transition_success_table = pd.read_sql(
            "SELECT * FROM transition_success", self.db.engine
        )
        self.actions_table = pd.read_sql("SELECT * FROM actions", self.db.engine)

        self.n_questions_to_consider = 5
        self.states = set([tr[0] for tr in self.shift_vectores_matrix])

    def get_user_state(self, uuid):
        """
        Find previous user state and select all possible state with their success probs.

        :param uuid: user id

        :return: list of probs for each next phrase and id of phrase.
                 [(phrase_id1, prob1), (phrase_id2, prob2)]
        """

        return  # TODO

    def step(self, action: int) -> Tuple[list, float, bool, dict]:
        """
        Perform a transition step among the questions

        :param action: Chosed transition from the agent's action space.

        :return: The tuple with parameters -
                 next state, reward, transition success status (done), transition info.
        """
        # TODO

        return  # TODO self.state, reward, done, {}

    def reset(self, seed: int = None) -> list[float]:
        """
        Reset state setting a new one randomly

        :param seed: The random seed for state generation.

        :return: the vector of the question state.
        """
        # TODO
