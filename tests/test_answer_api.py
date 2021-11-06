import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        # send answer
        rv = c.patch(
            "/answer",
            headers={
                "session_token": "47a60ef9e7337bf0",
            },
            json={
                "question_token": "09a6d97aee2f097e",
                "user_answer": "this is answer on second language",
            },
        )
        json_data = rv.get_json()
        score = json_data["score"]
        assert isinstance(score, float)
