from flask import url_for

ANSWER = {"alive": True}


def test_status(client):
    response = client.get(url_for('api_v1.get-status'))
    assert response.json == ANSWER
