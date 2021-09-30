import os
from typing import List


def normalize_form_of_answer(answer: str) -> str:
    """
    Normalize string to the single form which are
    equal in any case of writing style.
    """
    answer = answer.lower().strip()

    symbols_to_ignore = "!@#$%^&?,.:;"
    for symb in symbols_to_ignore:
        answer = answer.replace(symb, "")
    return answer


def tokenize_answer(language_model, answer: str) -> List:
    """
    Tokenize sentence
    """
    tokens = answer.split() if len(answer) > 0 else []
    return tokens


def get_equality_rate(
    language_model, language: str, user_answer: str, real_answer: str
) -> float:
    """
    Get equality_rate between users
    """
    user_answer_tokens = tokenize_answer(language_model, user_answer)
    real_answer_tokens = tokenize_answer(language_model, real_answer)
    if language in ["russian", "french", "ukrainian"]:
        equality_rate = sum(
            [u in real_answer_tokens for u in user_answer_tokens],
        )
        equality_rate = (
            2 * equality_rate / (len(real_answer_tokens) + len(user_answer_tokens))
        )
    elif language in ["english"]:
        equality_rate = sum(
            [u == r for u, r in zip(user_answer_tokens, real_answer_tokens)],
        )
        equality_rate = (
            2 * equality_rate / (len(real_answer_tokens) + len(user_answer_tokens))
        )
    else:
        raise ValueError(f"Unknown language <{language}>")
    return equality_rate


def compare_answers(
    language_model, language: str, real_answer: str, user_answer: str
) -> bool:
    """
    This function compares answer and makes an inference
    about of equality
    """
    user_answer = normalize_form_of_answer(user_answer)
    real_answer = normalize_form_of_answer(real_answer)

    equality_rate = get_equality_rate(
        language_model, language, user_answer, real_answer
    )
    is_equal = equality_rate >= 0.95

    comparing_result = {
        "is_equal": is_equal,
        "equality_rate": equality_rate,
    }
    return comparing_result
