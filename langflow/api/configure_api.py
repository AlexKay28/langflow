import json

from app import session
from . import api, request


@api.route("/configure", methods=["POST"])
def configure_api():
    """
    Start configuring user's session by means of initializations himself
    selecting the languages and level
    Endpoint gets the keys:
        first_language, second_language, level
    """
    # get params
    first_language = request.args["first_language"]
    second_language = request.args["second_language"]
    level = int(request.args["level"])

    # init user in session
    uuid_generated, user_existance = session.create_user(
        first_language, second_language, level
    )

    return json.dumps({"uuid": uuid_generated, "status": user_existance})
