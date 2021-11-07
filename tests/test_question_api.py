import json
import pytest


def test_question_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        rv = c.post(
            "/question",
            headers={
                "session_token": "37367bab4b0890b2",
            },
            json={
                "first_language": "english",
                "second_language": "french",
                "level": "1",
            },
        )
        json_data = rv.get_json()
        question_token = json_data["question_token"]
        assert not ask_valid_uuid(question_token) and len(question_token) == 16
