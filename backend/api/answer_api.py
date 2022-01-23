import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from utils.tips import show_differences

from . import api, session, db_controller


@api.route("/answer", methods=["PATCH"])
@swag_from("swaggers/answer_api.yml")
def answer_api():
    try:
        # auth token
        session_token = request.headers.get("session_token")
        # request body
        req = request.get_json()
        question_token = req["question_token"]
        user_answer = req["user_answer"]

        # get uuid using session_token
        uuid = session.get_user_uuid(session_token)
        quid = session.get_question_quid(question_token)

        # get info from db about users question
        flang, flang_phrase, slang, slang_phrase = session.get_user_phrases(uuid, quid)

        # apply models to compare answer and get inference
        comparing_result = session.compare_answers(slang, slang_phrase, user_answer)
        is_equal = comparing_result["is_equal"]
        score = comparing_result["equality_rate"]

        # records users success/fail in his metadata
        session.record_users_result(uuid, quid, user_answer, score)

        # update transition matrics on the fly
        db_controller.update_transitions(slang, uuid)

        # generate tips for user
        differences = ""
        if not is_equal:
            differences = show_differences(slang_phrase, user_answer)

        return jsonify(
            {
                "status": 200,
                "question": flang_phrase,
                "answer": slang_phrase,
                "answer_user": user_answer,
                "is_equal": is_equal,
                "score": score,
                "differences": differences,
            }
        )
    except Exception as e:
        return jsonify(
            {
                "status": 500,
                "message": f"Server internal error. {e}",
                "traceback": f"{traceback.format_exc()}",
            }
        )
