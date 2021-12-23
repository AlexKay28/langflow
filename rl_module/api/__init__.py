from flask import Blueprint

from src.environment import QuestionSpaceEnv
from src.agent import Agent


env = QuestionSpaceEnv()
agent = Agent()

api = Blueprint("api", __name__)

from .get_pair import get_pair_api
