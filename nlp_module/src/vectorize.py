import os
import fasttext
import numpy as np
from functools import lru_cache


PATH_TO_MODELS = "language_models/"


@lru_cache(maxsize=2)
def _load_language_model(model_name: str, extension: str = ".bin") -> object:
    """
    Load fasttext model

    :param model_name: name of model to upload for similarity comparing
    :param extension: the extenstion of the binary model file

    :return: loaded fasttext model
    """
    model_name_ext = f"{model_name}.bin"
    model_path = os.path.join(PATH_TO_MODELS, f"{model_name_ext}")
    return fasttext.load_model(model_path)


def get_phrase_vector(language: str, phrase: str) -> np.ndarray:
    """
    Get phrase vector using language model which provides each
    containing token embedding

    :param language: Defined language model name for similarity processing.
    :param phrase_tokens: The list of tokens which is going to be norlmalized.

    :return: The numpy array of aggregated vector
    """
    language_model = _load_language_model(language)

    # tokenization
    tokens = phrase.split() if len(phrase) > 0 else []

    # model apply
    token_vecs = np.array([language_model.get_word_vector(t) for t in tokens])

    # agg vecs
    phrase_vec = token_vecs.mean(axis=0)

    return phrase_vec
