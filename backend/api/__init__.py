import json
from flask import Blueprint

from utils.session_object import SessionController
from utils.db_controller import DbController

session = SessionController()
db_controller = DbController()

api = Blueprint("api", __name__)


@api.after_request
def after(response):
    # todo with response
    r = response.get_json()
    if r and r["status"] != 200:
        print("=" * 30, end="\n\n")
        print("Status code:", r["status"])
        print(r["traceback"])
        print("=" * 30)
    return response


from .authorization_api import authorization_api
from .login_api import login_api
from .question_api import question_api
from .answer_api import answer_api
from .results_api import results_api
from .upload_phrases import upload_phrases
