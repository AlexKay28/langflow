import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        session_token = next(iter(session.db.users))
        quid = next(iter(session.db.get_user(session_token).questions))
        # send answer
        rv = c.patch(
            "/answer",
            headers={
                "session_token": session_token,
            },
            json={
                "quid": quid,
                "user_answer": "this is answer on second language",
            },
        )
        json_data = rv.get_json()
        print(json_data)
        quid = json_data["quid"]
        assert ask_valid_uuid(quid)
