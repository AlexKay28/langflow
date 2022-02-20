import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, session


@api.route("/login", methods=["POST"])
@swag_from("swaggers/login_api.yml")
def login_api():
    try:
        req = request.get_json()
        username = req["username"]
        password = req["password"]
        is_anon = req["is_anon"]
        status, session_token_generated = session.activate_session_token(
            username, password, is_anon
        )
        return jsonify(
            {
                "status": status,
                "session_token": session_token_generated,
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
