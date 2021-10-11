import pytest
import json


def test_configure_api(client):
    """Start with a blank session."""
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    message = {
        "first_language": "english",
        "second_language": "french",
        "level": 1,
    }
    response = client.post(
        "configure",
        data=json.dumps({"title": "123", "body": "333"}),
        headers=headers,
    )
    print(response.__dict__)
    assert response == 1
