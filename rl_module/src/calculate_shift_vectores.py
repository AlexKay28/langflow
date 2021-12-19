import numpy as np
import pandas as pd
from ..utils.comaring import get_phrase_vector

PAHT_TO_PHRASES = "../tmp/phrases.csv"


def calculate_matrix():
    phrases = pd.read_csv(PAHT_TO_PHRASES)
    return  # TODO
