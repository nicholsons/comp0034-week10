import requests
from flask import url_for


def test_server_is_up_and_running(init_multiprocessing, live_server):
    response = requests.get(url_for("index", _external=True))
    assert b"Iris Home" in response.content
    assert response.status_code == 200
