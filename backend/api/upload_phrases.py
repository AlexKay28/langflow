import json
import pandas as pd
import traceback

from . import api, request, jsonify, session


@api.route("/phrases/file", methods=["POST"])
def upload_phrases():
    """
    Upload phrases to database using csv file
    provided to the current endpoint
    """
    try:
        # auth token
        session_token = request.headers.get("session_token")

        # data
        phrases_file = request.files["file"]

        # get uuid using session_token
        uuid = session.get_user_uuid(session_token)

        # TODO: check uuid belongs to admin

        # work with provided file
        phrases = pd.read_csv(phrases_file)
        if session.upload_phrases_to_db(phrases):
            raise Exception("Uploading phrases dataframe to database was failed!")

        return "Phrases was uploaded to database SUCCESSFULLY!"
    except Exception as e:
        return jsonify(
            {
                "status": 500,
                "message": f"Server internal error. {e}",
                "traceback": f"{traceback.format_exc()}",
            }
        )
