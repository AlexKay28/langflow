from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

from .configure_api import configure_api
from .question_api import question_api
from .answer_api import answer_api
from .results_api import results_api
