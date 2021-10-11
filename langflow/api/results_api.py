import json

from app import session
from . import api, request


@api.route("/results", methods=["POST"])
def results_api():
    """
    Final statistics about users progress while session
    Endpoint gets the keys:
        uuid
    """
    # get params
    uuid = request.args["uuid"]

    # calculate user's data analysis obtained while session
    analysis = session.get_user_analysis(uuid)

    return json.dumps(analysis)
