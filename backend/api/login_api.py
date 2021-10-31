import json

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

        if not is_anon:
            # user autorization to server.
            session_token_generated, user_existance = session.create_user(
                username, password
            )
        else:
            # user works anonymously
            session_token_generated, user_existance = session.create_user(
                username, password
            )

        return jsonify(
            {"session_token": session_token_generated, "status": user_existance}
        )
    except Exception as e:
        print(e)
        return jsonify({"status": 400, "message": f"Bad request. {e}"})
