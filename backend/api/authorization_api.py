import json
import traceback

from flask import request, jsonify
from flasgger.utils import swag_from

from . import api, session


@api.route("/authorization", methods=["POST"])
@swag_from("swaggers/authorization_api.yml")
def authorization_api():
    try:
        req = request.get_json()
        username = req["username"]
        password = req["password"]
        email = req["email"]
        status, result = session.create_user(username, password, email)
        return jsonify(
            {
                "status": status,
                "message": result,
                # TODO: needed for backend working if code != 200
                "traceback": f"Traceback is not needed.",
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
