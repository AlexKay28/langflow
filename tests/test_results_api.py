import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        rv = c.get(
            "/results",
            headers={
                "session_token": "8fcb4a81047dbeff",
            },
            json={},
        )
        json_data = rv.get_json()
        average_score = json_data["average_score"]
        assert isinstance(average_score, float)
