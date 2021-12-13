import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, session


@api.route("/results", methods=["GET"])
@swag_from("swaggers/results_api.yml")
def results_api():
    try:
        # auth token
        session_token = request.headers.get("session_token")

        # get uuid using session_token
        uuid = session.get_user_uuid(session_token)
        (
            slangs_counts,
            answered_questions_number,
            unanswered_questions_number,
            average_score,
            message,
        ) = session.get_user_analysis(uuid)

        return jsonify(
            {
                "status": 200,
                "target_languages_counts": slangs_counts,
                "answered_questions_number": answered_questions_number,
                "unanswered_questions_number": unanswered_questions_number,
                "average_score": average_score,
                "inference": message,
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
