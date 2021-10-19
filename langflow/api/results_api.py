import json

from . import api, request, jsonify, session


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

    # will be removed in #39
    # session.db.update_data()

    return jsonify(analysis)
