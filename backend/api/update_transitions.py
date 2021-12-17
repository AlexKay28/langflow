import traceback

from flask import jsonify, request
from flasgger.utils import swag_from

from . import api, db_controller


@api.route("/transitions", methods=["PATCH"])
@swag_from("swaggers/update_transitions.yml")
def update_transitions():
    """
    Update transition success matrix using actions table
    """
    try:
        # auth token
        session_token = request.headers.get("session_token")

        # work with provided file
        db_controller.update_transitions_global()
        message = "transitions updated!"
        return jsonify(
            {
                "status": 200,
                "message": message,
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
