import json
from urllib.request import urlopen

import pytest

from server import run_server_in_thread

PORT = 8089
TEST_DB = "data.sqlite"  # TODO: priprav v ramci testu


@pytest.fixture(scope="module")
def server():
    httpd, thread = run_server_in_thread(TEST_DB, PORT)
    yield f"http://{httpd.server_address[0]}:{httpd.server_address[1]}"
    httpd.shutdown()
    thread.join()


def test_status(server):
    with urlopen(f"{server}/status") as response:
        assert response.status == 200
        data = json.load(response)
        assert data == {"status": "ok"}


# def test_status(client):
#     response = client.get("/status")
#     assert response.status_code == 200
#     assert response.data == b'{"status":"ok"}\n'
