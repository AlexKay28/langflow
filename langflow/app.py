import json
import uuid

from utils.session import SessionController
from utils.comparing import compare_answers
from utils.tips import show_differences

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
session = SessionController()


@app.route("/", methods=["POST", "GET"])
def home_page():
    """
    Main page of LangFlow
    """
    if request.method == "POST":  # make GET
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["GET"])  # it will be removed soon
def practice_page():
    """
    Practicing page # make GET
    """
    return render_template("practice.html")


@app.route("/configure", methods=["POST"])
def configure_api():
    """
    Start configuring user's session by means of initializations himself
    selecting the languages and level
    Endpoint gets the keys:
        first_language, second_language, level
    """
    # get params
    first_language = request.args["first_language"]
    second_language = request.args["second_language"]
    level = int(request.args["level"])

    # init user in session
    uuid_generated, user_existance = session.create_user(
        uuid, first_language, second_language, level
    )

    return json.dumps({"uuid": uuid_generated, "status": user_existance})


@app.route("/question", methods=["POST"])
def question_api():
    """
    Generate question for particular user
    Endpoint gets the keys:
        uuid,
    """
    # get params
    uuid = request.args["uuid"]

    # smart question generation
    quid, first_language_phrase, second_language_phrase = session.generate_phrase_pair(
        uuid
    )

    return json.dumps(
        {
            "uuid": uuid,
            "quid": quid,
            "question": first_language_phrase,
            "answer": second_language_phrase,
        }
    )


@app.route("/answer", methods=["POST"])
def answer_api():
    """
    Evaluate users answer and return him the answer analysis back
    Endpoint gets the keys:
        uuid, qid, second_language_phrase_answer
    """
    # get params
    uuid = request.args["uuid"]
    quid = request.args["quid"]
    second_language_phrase_answer = request.args["second_language_phrase_answer"]

    # get question which was asked to user from his metadata
    first_language_phrase, second_language_phrase = session.get_user_phrases(uuid, quid)

    # apply models to compare answer and get inference
    model_to_apply = session.language_models[session.users[uuid].second_language]
    comparing_result = compare_answers(
        model_to_apply, second_language_phrase, second_language_phrase_answer
    )
    is_equal = comparing_result["is_equal"]
    equality_rate = comparing_result["equality_rate"]

    # records users success/fail in his metadata
    session.record_users_result(uuid, quid, equality_rate)

    # generate tips for user
    differences = ""
    if not is_equal:
        differences = show_differences(
            second_language_phrase, second_language_phrase_answer
        )

    return json.dumps(
        {
            "uuid": uuid,
            "quid": quid,
            "question": first_language_phrase,
            "answer": second_language_phrase,
            "answer_user": second_language_phrase_answer,
            "is_equal": is_equal,
            "score": equality_rate,
            "differences": differences,
        }
    )


@app.route("/results", methods=["POST"])
def results_api():
    """
    Final statistics about users progress while session
    Endpoint gets the keys:
        uuid
    """
    # get params
    uuid = request.args["uuid"]

    # calculate user's data analysis obtained while session
    analysis = session.get_user_analysis(uuid)

    return json.dumps(analysis)


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
