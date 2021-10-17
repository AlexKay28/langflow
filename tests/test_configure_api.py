import json
import pytest


def test_configure_status(client):
    with client.test_client() as c:
        rv = c.post(
            "/configure",
            json={
                "first_language": "english",
                "second_language": "french",
                "level": "1",
            },
        )
        json_data = rv.get_json()
        assert json_data["status"]


def test_configure_uuid(client, ask_valid_uuid):
    with client.test_client() as c:
        rv = c.post(
            "/configure",
            json={
                "first_language": "russian",
                "second_language": "ukrainian",
                "level": "2",
            },
        )
        json_data = rv.get_json()
        assert ask_valid_uuid(json_data["uuid"])
