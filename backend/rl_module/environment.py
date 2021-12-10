import numpy as np
from typing import Tuple


class QuestionSpace:
    """
    Description:
        Question space contains questions vectores of the same dimension
        represented as text embedding. The main goag of the environment is
        to represent question space as much clear and correct in terms of texts
        difficulty and similarity relation.
    Observation:
        Type:
        Num     Observation                   Representation
        0       The shift vector till
                the first closest question    (n_dim_vec)
        1       The shift vector till
                the second closest question   (n_dim_vec)
        2       The shift vector till
                the third closest question    (n_dim_vec)
        3       The shift vector till
                the fourth closest question   (n_dim_vec)
        4       The shift vector till
                the fifth closest question    (n_dim_vec)
    Actions:
        Type: Discrete(2)
        Num   Action
        0     Choose the first closest question
        1     Choose the second closest question
        2     Choose the third closest question
        3     Choose the fourth closest question
        4     Choose the fifth closest question
    Reward:
        Reward is between [0, 1] and estimated by semantic closeness
    Starting State:
        Randomly
    Episode Termination:
        Defined number of iteration and early stopped
    """

    def __init__(self):
        # shift vectores (length, angle, id)
        self.shift_vectores_matrix = [
            (0, 0, [0.0, 0.0, 0.0]),
            (0, 1, [1.0, 1.0, 0.0]),
            (0, 2, [1.0, 0.0, 1.0]),
            (1, 0, [-1.0, -1.0, 0.0]),
            (1, 1, [0.0, 0.0, 0.0]),
            (1, 2, [0.0, 1.0, 0.0]),
            (2, 0, [-1.0, 0.0, -1.0]),
            (2, 1, [1.0, -1.0, 0.0]),
            (2, 2, [0.0, 0.0, 0.0]),
        ]
        # successfullness transition matrix
        self.transition_success_matrix = [
            (0, 0, 0.38),
            (0, 1, 0.56),
            (0, 2, 0.75),
            (1, 0, 0.23),
            (1, 1, 0.99),
            (1, 2, 0.32),
            (2, 0, 0.04),
            (2, 1, 0.23),
            (2, 2, 0.82),
        ]

        self.n_questions_to_consider = 5
        self.states = set([tr[0] for tr in self.shift_vectores_matrix])

    def _get_appropriate_transitions(self, state_id: int) -> list[int]:
        """
        Get appropriate shift vectores to all positions from existed data
        :param state_id: interested state id
        :return: list of transitions
        """
        return [
            transition
            for transition in self.shift_vectores_matrix
            if tr[0] == state_id and tr[0] != tr[1]
        ]

    def _get_top_n_transitions(self, transitions: list, n_top: int) -> list[int]:
        """
        Sort transitions by vector closeness.

        :param transitions: All possible transitions from a state

        :return: N top closest transitions.
        """
        # sorted by length and selection of top n
        sorted_transitions = sorted(vecs, key=lambda tr: -1 * np.linalg.norm(tr[2]))
        return sorted_transitions[:n_top]

    def _get_user_answer_score(self, asked_question_id: int) -> float:
        """
        Get user obtained similarity score.

        :param asked_question_id: Id of asked by user question in list of questions.

        :return: Score gained by user.
        """
        return 1.0  # TODO

    def _update_transition_success_matrix(
        self, previous_state: list[float], next_state: list[float], reward: float
    ) -> None:
        """
        Update matrix using retrieved reward.

        :param previous_state: The state which already was answered by user.
        :param next_state: The next state from transition.
        :param reward: The answer closeness (reward) gained by user in the current state.
        """
        pass  # TODO

    def step(self, action: int) -> Tuple[list, float, bool, dict]:
        """
        Perform a transition step among the questions

        :param action: Chosed transition from the agent's action space.

        :return: The tuple with parameters -
                 next state, reward, transition success status (done), transition info.
        """
        # apply action and let user to gain reward
        previous_state, next_state, shift_vector = self.state[action]
        reward = slef._get_user_answer_score(next_state)

        # update success matrix
        self._update_transition_success_matrix(previous_state, next_state, reward)

        # change state
        all_possible_transitions = self._get_appropriate_transitions(next_state)

        # sort vecs
        self.state = self._get_top_n_transitions(
            all_possible_transitions, self.n_questions_to_consider
        )

        # still playing infinitely now
        done = True

        return self.state, reward, done, {}

    def reset(self, seed: int = None) -> list[float]:
        """
        Reset state setting a new one randomly

        :param seed: The random seed for state generation.

        :return: the vector of the question state.
        """
        # select random row with vectores
        random_state_id = np.random.choice(self.states)
        all_possible_transitions = self._get_appropriate_transitions(random_state_id)

        # sort vecs
        self.state = self._get_top_n_transitions(
            all_possible_transitions, self.n_questions_to_consider
        )
        return state
