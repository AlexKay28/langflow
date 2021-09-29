from main import SessionController
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
session = SessionController()


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Main page of LangFlow
    """
    if request.method == "POST":
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["POST", "GET"])
def home():
    """
    Practicing page
    """
    if request.method == "GET" or session.is_new_session:
        first_language_phrase, second_language_phrase = session.generate_phrase_pair()
        session.set_session_langs_phrases(first_language_phrase, second_language_phrase)
        return render_template(
            "practice_ask.html",
            first_language_phrase=first_language_phrase,
        )
    elif request.method == "POST" :
        first_language_phrase, second_language_phrase = session.get_session_langs_phrases()
        second_language_phrase_answer = request.form["second_language_phrase_answer"]
        return render_template(
            "practice_answer.html",
            first_language_phrase=first_language_phrase,
            second_language_phrase=second_language_phrase,
            second_language_phrase_answer=second_language_phrase_answer,
        )
    else:
        raise ValueError(f"Method <{request.method}> underfined!")


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
