from flask import Blueprint

from src.comparing import compare_answers

api = Blueprint("api", __name__)

from .get_similarity import get_similarity
