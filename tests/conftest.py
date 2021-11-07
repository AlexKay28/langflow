import sys
import pytest
from uuid import UUID
from flask import Flask, jsonify, request

sys.path.append("../backend")

from api import api
from dbase import db

from utils.session_object import SessionController


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:123456@localhost:5432/langflow"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
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
