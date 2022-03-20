from flask import Blueprint

from src.tips import show_differences
from src.comparing import compare_answers
from src.vectorize import get_phrase_vector

api = Blueprint("api", __name__)

from .get_similarity_api import get_similarity_api
from .get_phrase_vector_api import get_phrase_vector_api
