import re


def normalize_text(answer: str) -> str:
    """
    Normalize string to the single form which are
    equal in any case of writing style.

    :param answer: answer of user needed to normalize

    :return: normalized answer with replaced symbols
    """
    answer = answer.lower().strip()

    symbols_to_ignore = "!@#$%^&?,.:;"
    for symb in symbols_to_ignore:
        answer = answer.replace(symb, " ")

    answer = re.sub(r"\s+", " ", answer)

    return answer
