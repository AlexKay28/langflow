import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, env, agent


@api.route("/get_pair", methods=["POST"])
@swag_from("swaggers/get_pair_api.yml")
def get_pair_api():
    try:
        req = request.get_json()
        uuid = req["uuid"]
        second_language = req["second_language"]
        level = req["level"]

        # load tables from base with current user state
        current_state = env.get_user_state(uuid)

        # choose question
        phrase_id = agent(current_state, policy_type="e_greedy")

        # phrase_id, reward, done, info = env.step(action)

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
