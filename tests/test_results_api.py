import json
import pytest


def test_answer_uuid(client, session, ask_valid_uuid):
    with client.test_client() as c:
        uuid = next(iter(session.db.users))
        rv = c.post(
            "/results",
            json={
                "uuid": uuid,
            },
        )
        json_data = rv.get_json()
        uuid = json_data["uuid"]
        statistics = json_data["statistics"]
        assert json_data["statistics"] is not None and ask_valid_uuid(uuid)
