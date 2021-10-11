import json

from app import session
from . import api, request


@api.route("/question", methods=["POST"])
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
