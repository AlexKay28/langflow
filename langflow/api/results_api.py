import json

from app import session
from . import api, request, jsonify


@api.route("/results", methods=["POST"])
def results_api():
    """
    Final statistics about users progress while session
    Endpoint gets the keys:
        uuid
    """
    # get params
    req = request.get_json() if not request.args else request.args
    uuid = req["uuid"]

    # calculate user's data analysis obtained while session
    analysis = session.get_user_analysis(uuid)

    return jsonify(analysis)
