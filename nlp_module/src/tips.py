import difflib
from colorama import Fore, Style


def show_differences(real_answer: str, user_answer: str) -> str:
    """
    Function shows difference between the users answer and the correct one.

    :param real_answer: The answer from the base which is ideal for question.
    :param user_answer: The answer from user which should be compared with real_answer.

    :return: Colored string with correction tips.
    """
    fixed_string = ""
    difference_iterator = difflib.ndiff(real_answer, user_answer)

    previous_is_green = False
    for f in difference_iterator:
        if f[0] == " ":
            fixed_string += f[-1]
            previous_is_green = False
        # this is the case when wrong word has been written
        elif f[0] == "+" and not previous_is_green:
            fixed_string += f"{Fore.RED}{f[-1]}{Style.RESET_ALL}"
            previous_is_green = False
        # this is the case when wrong word has been missed
        elif f[0] == "-":
            fixed_string += f"{Fore.GREEN}{f[-1]}{Style.RESET_ALL}"
            previous_is_green = True

    return fixed_string
