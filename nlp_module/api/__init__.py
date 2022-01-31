from flask import Blueprint

from src.comparing import compare_answers
from src.tips import show_differences

api = Blueprint("api", __name__)

from .get_similarity import get_similarity
