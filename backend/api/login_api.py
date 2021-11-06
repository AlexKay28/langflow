import json
import traceback

from . import api, request, jsonify, session


@api.route("/login", methods=["POST"])
def login_api():
    """
    User login endpoint.
    """
    try:
        req = request.get_json()
        username = req["username"]
        password = req["password"]
        is_anon = req["is_anon"]
        session_token_generated, user_existance = session.activate_session_token(
            username, password, is_anon
        )
        return jsonify(
            {"session_token": session_token_generated, "status": user_existance}
        )
    except Exception as e:
        return jsonify(
            {
                "status": 500,
                "message": f"Server internal error. {e}",
                "traceback": f"{traceback.format_exc()}",
            }
        )
