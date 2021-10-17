import sys
import pytest
from uuid import UUID
from flask import Flask, jsonify, request

sys.path.append("../langflow")

from api import api
from utils.session_object import SessionController


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


@pytest.fixture
def session():
    session = SessionController()
    return session


@pytest.fixture
def ask_valid_uuid():
    # set function
    def is_valid_uuid(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    return is_valid_uuid
