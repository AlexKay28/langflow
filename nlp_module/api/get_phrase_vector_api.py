import os
import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, get_phrase_vector

INCORRECT_ANSWER_THRESHOLD = float(os.getenv('INCORRECT_ANSWER_THRESHOLD'))


@api.route("/get_phrase_vector", methods=["GET"])
@swag_from("swaggers/get_phrase_vector_api.yml")
def get_phrase_vector_api():
    try:
        req = request.get_json()
        language = req["language"]
        phrase = req["phrase"]

        vector = get_phrase_vector(language, phrase)

        return jsonify({"status": 200, "vector": str(vector)})

    except Exception as e:
        return jsonify(
            {
                "status": 500,
                "message": f"Server internal error. {e}",
                "traceback": f"{traceback.format_exc()}",
            }
        )
