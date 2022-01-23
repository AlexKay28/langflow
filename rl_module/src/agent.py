import numpy as np

EXPLORATION_RATE = 0.5


class Agent:
    def __init__(self):
        pass

    def __call__(self, current_state, policy_type="e_greedy"):
        phrase_ids_in_base = [i[0] for i in current_state]
        phrase_probs = [i[1] for i in current_state]

        if policy_type == "greedy":
            choosed_phrase = self.greedy_policy(phrase_probs)
        elif policy_type == "e_greedy":
            choosed_phrase = self.e_greedy_policy(phrase_probs)
        else:
            raise KeyError(f"Unknown policy type <{policy_type}>")

        return phrase_ids_in_base[choosed_phrase]

    def greedy_policy(self, action_space) -> int:
        return np.argmax(action_space)

    def e_greedy_policy(self, action_space) -> int:
        if np.random.random() < EXPLORATION_RATE:
            return np.random.choice(len(action_space))
        else:
            return np.argmax(action_space)
