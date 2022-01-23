import os
import gzip
import shutil
import gensim
import numpy as np
from scipy.spatial.distance import cosine

from typing import List

CORRECTNESS_RATE = 0.98

PATH_TO_MODELS = "language_models/"


def load_language_model(model_name: str, extension: str = ".bin"):
    """
    Load fasttext model

    :param model_name: name of model to upload for similarity comparing
    :param extension: the extenstion of the binary model file

    :return: loaded fasttext model
    """
    model_name_ext = f"{model_name}300_quantized.bin"
    model_path = os.path.join(PATH_TO_MODELS, f"{model_name_ext}")
    return gensim.models.fasttext.FastTextKeyedVectors.load(model_path)


def normalize_form_of_answer(answer: str) -> str:
    """
    Normalize string to the single form which are
    equal in any case of writing style.

    :param answer: answer of user needed to normalize

    :return: normalized answer with replaced symbols
    """
    answer = answer.lower().strip()

    symbols_to_ignore = "!@#$%^&?,.:;"
    for symb in symbols_to_ignore:
        answer = answer.replace(symb, "")
    return answer


def tokenize_answer(answer: str) -> List:
    """
    Tokenize sentence

    :param answer: the answer to tokenize

    :return: the list of tokens
    """
    tokens = answer.split() if len(answer) > 0 else []
    return tokens


def get_phrase_vector(language_model, phrase_tokens: List) -> np.ndarray:
    """
    Get phrase vector using language model which provides each
    containing token embedding

    :param language_model: defined language model for similarity processing
    :param phrase_tokens: the list of tokens which is going to be norlmalized

    :return: the numpy array of aggregated vector
    """
    return language_model[" ".join(phrase_tokens)]


def get_similarity(vec1: np.ndarray, vec2: np.ndarray, metric: str = "cosine") -> float:
    """
    Calculate semantic closeness using choosed metric function

    :param vec1: the vector of the first phrase
    :param vec2: the vector of the second phrase
    :param metric: the metric how to calculate vectors closeness

    :return: the distance between two provided n-dim vectors
    """
    if metric == "cosine":
        return 1 - cosine(vec1, vec2)
    raise ValueError(f"Unknown distance metric <{metric}>")


def get_phrase_shift_vector(language, phrase1: str, phrase2: str) -> list:
    """
    Get shift vector between phrases.
    """
    language_model = load_language_model(language)
    phrase1_vec = get_phrase_vector(language_model, tokenize_answer(phrase1))
    phrase2_vec = get_phrase_vector(language_model, tokenize_answer(phrase2))
    return phrase2_vec - phrase1_vec


def get_equality_rate(language_model, real_answer: str, user_answer: str) -> float:
    """
    Get equality_rate between users

    :param real_answer: the answer from the base which is ideal for question
    :param user_answer: the answer from user which should be compared with real_answer

    :return: the distance between two phrases which is vectorized
    """
    if not user_answer:
        return 0.0
    real_answer_tokens = tokenize_answer(real_answer)
    user_answer_tokens = tokenize_answer(user_answer)
    equality_rate = get_similarity(
        get_phrase_vector(language_model, real_answer_tokens),
        get_phrase_vector(language_model, user_answer_tokens),
    )
    return equality_rate


def compare_answers(language, real_answer: str, user_answer: str) -> bool:
    """
    This function compares answer and makes an inference
    about of equality. The similarity threshold is defined by system

    :param real_answer: the answer from the base which is ideal for question
    :param user_answer: the answer from user which should be compared with real_answer

    :return: calculated inference about answer correctness
    """
    language_model = load_language_model(language)
    real_answer = normalize_form_of_answer(real_answer)
    user_answer = normalize_form_of_answer(user_answer)

    equality_rate = get_equality_rate(language_model, real_answer, user_answer)
    is_equal = 1 if equality_rate >= CORRECTNESS_RATE else 0

    comparing_result = {
        "is_equal": is_equal,
        "equality_rate": equality_rate,
    }
    return comparing_result
