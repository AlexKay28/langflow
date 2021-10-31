import json
import pytest


def test_question_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:

        session_token = next(iter(session.db.users))
        rv = c.post(
            "/question",
            headers={
                "session_token": session_token,
            },
            json={
                "first_language": "english",
                "second_language": "french",
                "level": "1",
            },
        )
        json_data = rv.get_json()
        quid = json_data["quid"]
        assert ask_valid_uuid(quid)
