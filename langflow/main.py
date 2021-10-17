import os
import sys
import numpy as np
from colorama import Fore, Style
from collections import Counter

from utils.tips import show_differences
from utils.session import SessionController
from utils.comparing import compare_answers

# Programm iterates over existed data and
# shows you sentences which should be translated
# by you
SESSION_PHRASES_COUNTER = 15
LEARNING_LANGS = {
    1: "english",
    2: "russian",
    3: "french",
    4: "ukrainian",
}
AVAILABLE_LEVELS = {0: "all levels", 1: "level 1", 2: "level 2"}


def get_session_terminal(first_language="english", second_language="french", level=0):
    """
    Session itself. User choose session_learning_language parameter
    which defines which dataset to use for known and learning language
    """

    session = SessionController()
    uuid, status = session.create_user(first_language, second_language, level)
    assert status

    bad_answers_counter = Counter()
    actions_counter = 0
    user_answer = None
    while 1:
        actions_counter += 1
        (
            quid,
            first_language_phrase,
            second_language_phrase_answer,
        ) = session.generate_phrase_pair(uuid)

        phrase = f"{Fore.YELLOW}{first_language_phrase}{Style.RESET_ALL}"
        print(f"{{:<25}}>> {{}}".format(f"Phrase #{actions_counter}", phrase))
        print(f"{{:<25}}>> ".format("Translate"), end="")
        user_answer = input()

        comparing_result = compare_answers(
            second_language,
            second_language_phrase_answer,
            user_answer,
        )

        if comparing_result["is_equal"]:
            second_language_phrase_answer = (
                f"{Fore.GREEN}{second_language_phrase_answer}{Style.RESET_ALL}"
            )
            print(f"{{:<25}}\n".format("Right answer!"), end="")
        else:
            bad_answers_counter.update(
                [f"{first_language_phrase}->{second_language_phrase_answer}"]
            )
            differences = show_differences(second_language_phrase_answer, user_answer)
            print(f"{{:<25}}>> {{}} ".format("Bad answer", differences))
            print(
                f"{{:<25}}   (Equality rate: {{}})".format(
                    "", round(comparing_result["equality_rate"], 3)
                )
            )
            print(f"{{:<25}}>> ".format("Repeat please"), end="")
            differences = show_differences(second_language_phrase_answer, input())
            print(f"{{:<25}}>> {{}}".format("Well!", differences))
        print()

        if actions_counter == SESSION_PHRASES_COUNTER:

            # Show 5 most frequent errors
            print("While practicing the most common mistakes:")
            for bad_answer, n_errors in bad_answers_counter.most_common(5):
                bad_answer_first, bad_answer_second = bad_answer.split("->")
                print(
                    f"({n_errors}) {Fore.YELLOW}{bad_answer_first}{Style.RESET_ALL} "
                    + f": {Fore.GREEN}{bad_answer_second}{Style.RESET_ALL}"
                )

            print("\nWould you like to keep practicing?)")
            print("Press y/N")
            if input() != "y":
                return 0
            print("Ok! Here we go!)")
            actions_counter = 0


def main():
    """
    Welcomes user and launch session with choosed setting
    """
    print(
        f"""\
    Hello! Choose language pair you want to learn!
    Among next available languages:
    {LEARNING_LANGS}

    and starting level:
    {AVAILABLE_LEVELS}
    """
    )
    first_language = LEARNING_LANGS[int(input("First language id : ") or "1")]
    second_language = LEARNING_LANGS[int(input("Second language id: ") or "3")]
    level = int(input("Level id: ") or "0")
    print(
        f"Cool! You have choosed: {Fore.GREEN}[{first_language}-{second_language}]{Style.RESET_ALL} "
        f"with level {Fore.GREEN}[{level}]{Style.RESET_ALL}"
    )
    try:
        get_session_terminal(first_language, second_language, level=level)
        print("Well, session is DONE then! Good luck!")
    except KeyboardInterrupt:
        print("\nStopping session softly.")


if __name__ == "__main__":
    main()
