import json

from . import api, request, jsonify, session


@api.route("/results", methods=["GET"])
def results_api():
    """
    Final statistics about users progress while session
    Endpoint gets the keys:
        uuid
    """
    try:
        # auth
        session_token = request.headers.get("session_token")

        # get uuid using session_token
        uuid = session_token

        analysis = session.get_user_analysis(uuid)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"status": 500, "message": f"Internal Server Error. {e}"})
