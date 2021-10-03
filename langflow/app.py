import json
from main import generate_phrase_pair
from utils.session import SessionController

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
session = SessionController(first_language="english", second_language="french", level=0)


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Main page of LangFlow
    """
    if request.method == "POST":  # make GET
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["POST", "GET"])
def home():
    """
    Practicing page
    """
    if request.method == "GET" or session.is_new_session:
        first_language_phrase, second_language_phrase = generate_phrase_pair(
            session.get_pairs()
        )
        session.set_session_langs_phrases(first_language_phrase, second_language_phrase)
        return render_template(
            "practice_ask.html",
            first_language_phrase=first_language_phrase,
        )
    elif request.method == "POST":
        (
            first_language_phrase,
            second_language_phrase,
        ) = session.get_session_langs_phrases()
        second_language_phrase_answer = request.form["second_language_phrase_answer"]
        return render_template(
            "practice_answer.html",
            first_language_phrase=first_language_phrase,
            second_language_phrase=second_language_phrase,
            second_language_phrase_answer=second_language_phrase_answer,
        )
    else:
        raise ValueError(f"Method <{request.method}> underfined!")


@app.route("/question", methods=["GET"])
def question():
    first_language_phrase, second_language_phrase = generate_phrase_pair(
        session.get_pairs()
    )
    session.set_session_langs_phrases(first_language_phrase, second_language_phrase)
    return json.dumps(
        {
            "qid": None,
            "question": first_language_phrase,
            "answer": second_language_phrase,
        }
    )


@app.route("/answer", methods=["POST"])
def answer():
    first_language_phrase, second_language_phrase = session.get_session_langs_phrases()
    second_language_phrase_answer = request.form["second_language_phrase_answer"]

    score = 1  # python code (server side)

    return json.dumps(
        {
            "question": first_language_phrase,
            "answer": second_language_phrase,
            "answer_user": second_language_phrase_answer,
            "score": score,
        }
    )


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
