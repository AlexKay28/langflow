import json
import pytest


def test_question_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:

        uuid = next(iter(session.db.users))
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
