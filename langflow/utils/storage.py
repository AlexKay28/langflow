import os
import pickle
import pandas as pd

PATH_TO_DATA = "data/"


class StorageDB:
    def __init__(self):
        path_to_users = os.path.join(PATH_TO_DATA, "users.pkl")
        path_to_phrases = os.path.join(PATH_TO_DATA, "phrases.csv")

        # is equal to connection establishing
        if os.path.exists(path_to_users):
            with open(path_to_users, "rb") as users_data:
                self.users = pickle.load(users_data)
        else:
            self.users = {}

        self.pairs = pd.read_csv(path_to_phrases)

    # Language phrases DB section
    def get_pairs(self):
        return self.pairs

    # Users DB section
    @property
    def users_uuid_list(self):
        return self.users.keys()

    def reset_users(self):
        self.users = {}

    def add_user(self, uuid, user_object):
        self.users[uuid] = user_object

    def get_user(self, uuid):
        return self.users[uuid]
