import os
import pytest

#
from flask import Flask
from utils.session import SessionController


@pytest.fixture
def client():
    yield Flask(__name__)


@pytest.fixture
def session():
    return SessionController()
