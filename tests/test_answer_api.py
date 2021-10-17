import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        uuid = next(iter(session.db.users))
        quid = next(iter(session.db.get_user(uuid).questions))
        # send answer
        rv = c.post(
            "/question",
            json={
                "uuid": uuid,
                "quid": quid,
            },
        )
        json_data = rv.get_json()
        uuid = json_data["uuid"]
        quid = json_data["quid"]
        assert ask_valid_uuid(uuid) and ask_valid_uuid(quid)
