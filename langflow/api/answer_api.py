import json

from app import session
from utils.tips import show_differences
from utils.comparing import compare_answers

from . import api, request


@api.route("/answer", methods=["POST"])
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
