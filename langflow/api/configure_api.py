import json

from . import api, request, jsonify, session


@api.route("/configure", methods=["POST"])
def configure_api():
    """
    Start configuring user's session by means of initializations himself
    selecting the languages and level
    Endpoint gets the keys:
        first_language, second_language, level
    """
    # get params
    req = request.get_json() if not request.args else request.args
    first_language = req["first_language"]
    second_language = req["second_language"]
    level = int(req["level"])

    # init user in session
    uuid_generated, user_existance = session.create_user(
        first_language, second_language, level
    )

    return jsonify({"uuid": uuid_generated, "status": user_existance})
