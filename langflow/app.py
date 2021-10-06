import json
import uuid

from utils.choosing import generate_phrase_pair
from utils.session import SessionController
from utils.comparing import compare_answers
from utils.tips import show_differences

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
session = SessionController(first_language="english", second_language="french", level=0)


@app.route("/", methods=["POST", "GET"])
def home_page():
    """
    Main page of LangFlow
    """
    if request.method == "POST":  # make GET
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["GET"])
def practice_page():
    """
    Practicing page
    """
    return render_template("practice.html")


@app.route("/question", methods=["GET"])
def question_api():
    first_language_phrase, second_language_phrase = generate_phrase_pair(
        session.get_pairs()
    )
    uuid_generated = str(uuid.uuid4())

    session.set_session_langs_phrases(
        uuid_generated,
        first_language_phrase,
        second_language_phrase,
    )
    return json.dumps(
        {
            "uuid": uuid_generated,
            "question": first_language_phrase,
            "answer": second_language_phrase,
        }
    )


@app.route("/answer", methods=["POST"])
def answer_api():
    uuid = request.args["uuid"]
    second_language_phrase_answer = request.args["second_language_phrase_answer"]
    first_language_phrase, second_language_phrase = session.get_session_langs_phrases(
        uuid
    )
    comparing_result = compare_answers(
        session.language_model,
        second_language_phrase,
        second_language_phrase_answer,
    )
    is_equal = comparing_result["is_equal"]
    equality_rate = comparing_result["equality_rate"]

    differences = ""
    if not is_equal:
        differences = show_differences(
            second_language_phrase,
            second_language_phrase_answer,
        )

    return json.dumps(
        {
            "question": first_language_phrase,
            "answer": second_language_phrase,
            "answer_user": second_language_phrase_answer,
            "is_equal": is_equal,
            "score": equality_rate,
            "differences": differences,
        }
    )


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
