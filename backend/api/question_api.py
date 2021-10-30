import json

from . import api, request, jsonify, session


@api.route("/question", methods=["POST"])
def question_api():
    """
    Generate question for particular user
    Endpoint gets the keys:
        uuid,
    """
    try:
        req = request.get_json()
        session_token = req["session_token"]
        first_language = req["first_language"]
        second_language = req["second_language"]
        level = int(req["level"])

        # get uuid using session_token
        uuid = session_token

        (
            quid,
            first_language_phrase,
            second_language_phrase,
        ) = session.generate_phrase_pair(uuid, first_language, second_language, level)
        return jsonify(
            {
                "quid": quid,
                "question": first_language_phrase,
                "answer": second_language_phrase,
            }
        )
    except Exception as e:
        return jsonify({"status": 400, "message": f"Bad request. {e}"})
