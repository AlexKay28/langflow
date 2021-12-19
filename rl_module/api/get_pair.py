import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, env, agent


@api.route("/get_pair", methods=["GET"])
@swag_from("swaggers/get_pair_api.yml")
def get_pair_api():
    try:
        req = request.get_json()
        uuid = req["uuid"]
        second_language = req["second_language"]
        level = req["level"]

        current_state = env.get_user_state(uuid)
        action = agent(current_state, policy_type="greedy")

        phrase_id, reward, done, info = env.step(action)

        return jsonify(
            {
                "status": 200,
                "phrase_id": phrase_id,
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
