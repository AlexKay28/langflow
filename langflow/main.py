import os
import sys
import numpy as np
import pandas as pd
from colorama import Fore, Style

from collections import Counter
from utils.tips import show_differences
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


class SessionController:

    """
    Session object which contains session parameters
    for correct question formatting and question selection
    """

    def __init__(self, first_language="english", second_language="french", level=0):
        self.first_language = first_language
        self.second_language = second_language
        self.level = level
        self.pairs = pd.read_csv(
            f"data/phrases.csv",
            usecols=["level", self.first_language, self.second_language],
        )
        print(self.pairs.columns)
        self.pairs = self.pairs[
            self.pairs.level.apply(lambda l: l == level if level > 0 else True)
        ][[self.first_language, self.second_language]].values

        # highly dynamic variables
        self.first_language_phrase = None
        self.second_language_phrase_answer = None

    @property
    def is_new_session(self):
        if not self.first_language_phrase and not self.first_language_phrase:
            return True
        return False

    def get_session_langs_phrases(self):
        return self.first_language_phrase, self.second_language_phrase_answer

    def set_session_langs_phrases(
        self, first_language_phrase, second_language_phrase_answer
    ):
        self.first_language_phrase = first_language_phrase
        self.second_language_phrase_answer = second_language_phrase_answer

    def generate_phrase_pair(self):
        return self.pairs[np.random.choice(len(self.pairs))]


def get_session(first_language, second_language, level):
    """
    Session itself. User choose session_learning_language parameter
    which defines which dataset to use for known and learning language
    """
    session = SessionController(
        first_language=first_language, second_language=second_language, level=level
    )
    bad_answers_counter = Counter()
    actions_counter = 0
    user_answer = None
    while 1:
        actions_counter += 1
        (
            first_language_phrase,
            second_language_phrase_answer,
        ) = session.generate_phrase_pair()
        phrase = f"{Fore.YELLOW}{first_language_phrase}{Style.RESET_ALL}"
        print(f"{{:<25}}>> {{}}".format(f"Phrase #{actions_counter}", phrase))
        print(f"{{:<25}}>> ".format("Translate"), end="")
        user_answer = input()

        comparing_result = compare_answers(
            second_language, second_language_phrase_answer, user_answer
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
                    "", comparing_result["equality_rate"]
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
        f"\with {Fore.GREEN}level[{level}]{Style.RESET_ALL}"
    )
    try:
        get_session(first_language, second_language, level=level)
        print("Well, session is DONE then! Good luck!")
    except KeyboardInterrupt:
        print("\nStopping session softly.")


if __name__ == "__main__":
    main()
