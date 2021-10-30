import json
import pytest


def test_configure_status(client):
    with client.test_client() as c:
        rv = c.post(
            "/login",
            json={
                "username": "username",
                "password": "password",
            },
        )
        json_data = rv.get_json()
        assert json_data["status"]


def test_configure_uuid(client, ask_valid_uuid):
    with client.test_client() as c:
        rv = c.post(
            "/login",
            json={
                "username": "username",
                "password": "password",
            },
        )
        json_data = rv.get_json()
        assert ask_valid_uuid(json_data["session_token"])
