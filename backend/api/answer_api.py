import json

from utils.tips import show_differences
from utils.comparing import compare_answers

from . import api, request, jsonify, session


@api.route("/answer", methods=["PATCH"])
def answer_api():
    """
    Evaluate users answer and return him the answer analysis back
    Endpoint gets the keys:
        uuid, qid, second_language_phrase_answer
    """
    try:
        # auth
        session_token = request.headers.get("session_token")

        req = request.get_json()
        quid = req["quid"]
        user_answer = req["user_answer"]

        # get uuid using session_token
        uuid = session_token

        (
            first_language,
            first_language_phrase,
            second_language,
            second_language_phrase,
        ) = session.get_user_phrases(uuid, quid)

        # apply models to compare answer and get inference
        comparing_result = compare_answers(
            second_language, second_language_phrase, user_answer
        )
        is_equal = comparing_result["is_equal"]
        equality_rate = comparing_result["equality_rate"]

        # records users success/fail in his metadata
        session.record_users_result(uuid, quid, equality_rate)

        # generate tips for user
        differences = ""
        if not is_equal:
            differences = show_differences(second_language_phrase, user_answer)

        return jsonify(
            {
                "quid": quid,
                "question": first_language_phrase,
                "answer": second_language_phrase,
                "answer_user": user_answer,
                "is_equal": is_equal,
                "score": equality_rate,
                "differences": differences,
            }
        )
    except Exception as e:
        return jsonify({"status": 500, "message": f"Internal Server Error. {e}"})
