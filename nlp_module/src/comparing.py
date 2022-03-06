import os
import numpy as np
from scipy.spatial import distance
from Levenshtein import jaro_winkler

from src.preprocessing import normalize_text
from src.vectorize import _load_language_model, get_phrase_vector

CORRECTNESS_RATE = float(os.getenv('CORRECTNESS_RATE'))
INCORRECT_ANSWER_THRESHOLD = float(os.getenv('INCORRECT_ANSWER_THRESHOLD'))
FIRST_MODEL_THRESHOLD = float(os.getenv('FIRST_MODEL_THRESHOLD'))


_PREFIX_WEIGHT = 0.05


def get_similarity(
    vec1: np.ndarray, vec2: np.ndarray, metric: str = "euclidean"
) -> float:
    """
    Calculate semantic closeness using choosed metric function

    :param vec1: the vector of the first phrase
    :param vec2: the vector of the second phrase
    :param metric: the metric how to calculate vectors closeness

    :return: the distance between two provided n-dim vectors
    """
    if metric == "cosine":
        return 1 - distance.cosine(vec1, vec2)
    elif metric == "euclidean":
        return np.exp(-distance.euclidean(vec1, vec2))
    elif metric == "manhattan":
        return np.exp(-distance.cityblock(vec1, vec2))
    raise ValueError(f"Unknown distance metric <{metric}>")


def get_phrase_shift_vector(language: str, phrase1: str, phrase2: str) -> list:
    """
    Get shift vector between phrases.
    """
    language_model = _load_language_model(language)
    phrase1_vec = get_phrase_vector(language_model, phrase1)
    phrase2_vec = get_phrase_vector(language_model, phrase2)
    return phrase2_vec - phrase1_vec


def compare_answers(language: str, real_answer: str, user_answer: str) -> dict:
    """
    This function compares answer and makes an inference
    about of equality. The similarity threshold is defined by system

    :param real_answer: the answer from the base which is ideal for question
    :param user_answer: the answer from user which should be compared with real_answer

    :return: calculated inference about answer correctness
    """
    real_answer = normalize_text(real_answer)
    user_answer = normalize_text(user_answer)

    # calculate fast-perfomance comparing.
    first_score = jaro_winkler(real_answer, user_answer, _PREFIX_WEIGHT)

    # if first score is obviously low - skip nlp check.
    if first_score < INCORRECT_ANSWER_THRESHOLD:
        equality_rate = 0.0
    elif first_score < FIRST_MODEL_THRESHOLD:
        equality_rate = first_score
    else:
        language_model = _load_language_model(language)
        v1 = get_phrase_vector(language_model, real_answer)
        v2 = get_phrase_vector(language_model, user_answer)
        equality_rate = get_similarity(v1, v2)

    is_equal = 1 if equality_rate >= CORRECTNESS_RATE else 0

    comparing_result = {
        "is_equal": is_equal,
        "equality_rate": equality_rate,
    }
    return comparing_result
