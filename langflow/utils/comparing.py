import os


def normalize_form_of_answer(answer: str) -> str:
    """
    Normalize string to the single form which are
    equal in any case of writing style.
    """
    answer = answer.lower()
    answer = answer.strip()

    symbols_to_ignore = "!@#$%^&?,.:;"
    for symb in symbols_to_ignore:
        answer = answer.replace(symb, "")

    return answer


def compare_answers(real_answer: str, user_answer: str) -> bool:
    """
    This function compares answer and makes an inference
    about of equality
    """
    user_answer = normalize_form_of_answer(user_answer)
    real_answer = normalize_form_of_answer(real_answer)
    return user_answer == real_answer
