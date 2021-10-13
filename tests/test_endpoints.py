import json
import pytest


def test_endpoints_existance(client):
    rules = [
        "api.configure_api",
        "api.question_api",
        "api.answer_api",
        "api.results_api",
    ]
    print(client.__dict__)
    for rule in client.url_map.iter_rules():

        if "static" in rule.endpoint:
            continue
        assert rule.endpoint in rules
