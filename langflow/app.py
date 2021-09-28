from main import get_languages_pair
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


class Session:
    asked_first_language = None
    asked_second_language = None


s = Session()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        first_language = s.asked_first_language
        second_language = s.asked_second_language
        second_language_answer = request.form["second_language_answer"]
        return render_template(
            "practice_answer.html",
            first_language=first_language,
            second_language=second_language,
            second_language_answer=second_language_answer,
        )
    else:
        first_language, second_language = get_languages_pair(
            "english",
            "french",
            "level1",
        )
        s.asked_first_language = first_language
        s.asked_second_language = second_language
        return render_template(
            "practice_ask.html",
            first_language=first_language,
        )


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
