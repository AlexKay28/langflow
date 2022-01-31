import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, compare_answers, show_differences


@api.route("/get_similarity", methods=["GET"])
@swag_from("swaggers/get_similarity_api.yml")
def get_similarity():
    try:
        req = request.get_json()
        language = req["language"]
        phrase1 = req["phrase1"]
        phrase2 = req["phrase2"]

        # compare_phrases
        comparing_result = compare_answers(language, phrase1, phrase2)
        is_equal = comparing_result["is_equal"]
        equality_rate = comparing_result["equality_rate"]

        # generate tips for user
        differences = ""
        if not is_equal:
            differences = show_differences(phrase1, phrase2)

        return jsonify(
            {
                "status": 200,
                "is_equal": is_equal,
                "equality_rate": equality_rate,
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
