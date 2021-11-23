from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from

from utils.session_object import SessionController

session = SessionController()
api = Blueprint("api", __name__)

from .authorization_api import authorization_api
from .login_api import login_api
from .question_api import question_api
from .answer_api import answer_api
from .results_api import results_api
from .upload_phrases import upload_phrases
