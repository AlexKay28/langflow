import numpy as np


class Agent:
    def __init__(self):
        pass

    def policy(self, action_space):
        return np.argmax(Q_table[state])
