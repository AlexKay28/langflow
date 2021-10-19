import json

from . import api, request, jsonify, session


@api.route("/question", methods=["POST"])
def question_api():
    """
    Generate question for particular user
    Endpoint gets the keys:
        uuid,
    """
    # get params
    req = request.get_json() if not request.args else request.args
    uuid = req["uuid"]

    # smart question generation
    quid, first_language_phrase, second_language_phrase = session.generate_phrase_pair(
        uuid
    )

    return jsonify(
        {
            "uuid": uuid,
            "quid": quid,
            "question": first_language_phrase,
            "answer": second_language_phrase,
        }
    )
