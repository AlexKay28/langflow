import json

from . import api, request, jsonify, session


@api.route("/login", methods=["POST"])
def login_api():
    """
    User login endpoint.
    """
    try:
        if request.method == "POST":
            # get login params
            req = request.get_json()
            username = req["username"]
            password = req["password"]

            # init user in session
            session_token_generated, user_existance = session.create_user(
                username, password
            )
            return jsonify(
                {"session_token": session_token_generated, "status": user_existance}
            )
        else:
            return jsonify(
                {
                    "status": 405,
                    "message": f"This method is not allowed for the requested URL",
                }
            )
    except Exception as e:
        print(e)
        return jsonify({"status": 400, "message": f"Bad request. {e}"})
