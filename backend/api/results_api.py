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
        if request.method == "GET":
            req = request.get_json()
            uuid = req["session_token"]
            analysis = session.get_user_analysis(uuid)
            return jsonify(analysis)
        else:
            return jsonify(
                {
                    "status": 405,
                    "message": f"This method is not allowed for the requested URL",
                }
            )
    except Exception as e:
        return jsonify({"status": 500, "message": f"Internal Server Error. {e}"})
