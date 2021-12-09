import numpy as np


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
                the first closest question    (length, angle, id)
        1       The shift vector till
                the second closest question   (length, angle, id)
        2       The shift vector till
                the third closest question    (length, angle, id)
        3       The shift vector till
                the fourth closest question   (length, angle, id)
        4       The shift vector till
                the fifth closest question    (length, angle, id)
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
        self.n_questions_to_consider = 5

        # shift vectores (length, angle, id)
        self.shift_vectores_matrix = [
            [(0, 0, 0), (0.76, 0.14, 1), (0.54, -0.43, 2)],
            [(0.34, 0.53, 0), (0, 0, 1), (0.43, -0.66, 2)],
            [(0.91, 0.92, 0), (0.76, -0.04, 1), (0, 0, 2)],
        ]
        # successfullness transition matrix
        self.transition_success_matrix = [
            [(float("-inf"), 0), (0.54, 1), (0.33, 2)],
            [(0.22, 0), (float("-inf"), 1), (0.87, 2)],
            [(0.92, 0), (0.66, 1), (float("-inf"), 2)],
        ]

    def _get_user_answer_score(self, asked_question_id):
        return 1

    def step(self, action):
        # apply action and let user to gain reward
        next_state_id = self.state[action][2]
        reward = slef._get_user_answer_score(next_state_id)

        # change state
        closest_vecs = self.shift_vectores_matrix[next_state_id]
        del realative_vecs[next_state_id]

        # sort vecs
        self.state = self._get_top_n_vectores(
            relations_to_other_vecs, self.n_questions_to_consider
        )

        # still playing infinitely now
        done = True

        return next_state, reward, done, {}

    def _get_top_n_vectores(self, vecs, n_top):
        # sorted by length and selection of top n
        vecs = sorted(vecs, key=lambda vec: -vec[0])[:n_top]
        return vecs

    def reset(self, seed: int = None):
        # select random row with vectores
        random_state_id = np.random.choice(len(self.shift_vectores_matrix))
        realative_vecs = self.shift_vectores_matrix[random_state_id]
        del realative_vecs[random_state_id]

        # sort vecs
        self.state = self._get_top_n_vectores(
            relations_to_other_vecs, self.n_questions_to_consider
        )
        return state
