import numpy as np

EXPLORATION_RATE = 0.65


class Agent:
    def __init__(self):
        pass

    def __call__(self, current_state, policy_type="e_greedy"):
        """
        state = {
            "user": user_vec,
            "idx": phrase_idx,
            "phrases": phrase_vec,
            "distances": dists
        }
        """
        user = current_state["user"]
        idxs = current_state["idx"]
        phrases = current_state["phrases"]
        distances = current_state["distances"]

        # flatten array
        idxs = idxs.squeeze()
        distances = distances.squeeze()

        # take softmax
        phrase_probs = 1 - np.exp(distances) / sum(np.exp(distances))

        if policy_type == "greedy":
            choosed_phrase = self.greedy_policy(phrase_probs)
        elif policy_type == "e_greedy":
            choosed_phrase = self.e_greedy_policy(phrase_probs)
        else:
            raise KeyError(f"Unknown policy type <{policy_type}>")

        return idxs[choosed_phrase]

    def greedy_policy(self, action_space) -> int:
        return np.argmax(action_space)

    def e_greedy_policy(self, action_space) -> int:
        if np.random.random() < EXPLORATION_RATE:
            return np.random.choice(len(action_space))
        else:
            return np.argmax(action_space)
