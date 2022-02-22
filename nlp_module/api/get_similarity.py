import os
import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, compare_answers, show_differences

INCORRECT_ANSWER_THRESHOLD = float(os.getenv('INCORRECT_ANSWER_THRESHOLD'))


@api.route("/get_similarity", methods=["GET"])
@swag_from("swaggers/get_similarity_api.yml")
def get_similarity():
    try:
        req = request.get_json()
        language = req["language"]
        correct_phrase = req["phrase1"]
        comparing_phrase = req["phrase2"]

        # compare_phrases
        comparing_result = compare_answers(language, correct_phrase, comparing_phrase)
        is_equal = comparing_result["is_equal"]
        equality_rate = comparing_result["equality_rate"]

        # generate tips for user
        differences = f"{correct_phrase}"
        if equality_rate > INCORRECT_ANSWER_THRESHOLD:
            differences = show_differences(correct_phrase, comparing_phrase)

        return jsonify(
            {
                "status": 200,
                "is_equal": is_equal,
                "equality_rate": equality_rate,
                "differences": "",
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
