import numpy as np

EXPLORATION_RATE = 0.1


class Agent:
    def __init__(self):
        pass

    def __call__(self, current_state, policy_type="greedy"):
        if policy_type == "greedy":
            return self.greedy_policy(current_state)
        elif policy_type == "e_greedy":
            return self.e_greedy_policy(current_state)
        else:
            raise KeyError(f"Unknown policy type <{policy_type}>")

    def greedy_policy(self, action_space):
        return np.argmax(action_space)

    def e_greedy_policy(self, action_space):
        if np.random.random() < EXPLORATION_RATE:
            return np.random.choice(len(action_space))
        else:
            return np.argmax(action_space)
