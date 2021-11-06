import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        # send answer
        rv = c.patch(
            "/answer",
            headers={
                "session_token": "3f2c077d1a8f731d",
            },
            json={
                "question_token": "693e2c6e3466654a",
                "user_answer": "this is answer on second language",
            },
        )
        json_data = rv.get_json()
        score = json_data["score"]
        assert isinstance(score, float)
