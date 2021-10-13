import json
import pytest


def test_question_uuid(client, session, ask_valid_uuid):
    print(session.users)
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
        uuid = json_data["uuid"]

        rv = c.post(
            "/question",
            json={
                "uuid": uuid,
            },
        )
        json_data = rv.get_json()
        uuid = json_data["uuid"]
        quid = json_data["quid"]
        assert ask_valid_uuid(uuid) and ask_valid_uuid(quid)
