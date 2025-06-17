import json
from http.client import HTTPConnection

import pytest

from server import run_server_in_thread

PORT = 8089
TEST_DB = "data.sqlite"  # TODO: priprav v ramci testu


@pytest.fixture(scope="module")
def server():
    httpd, thread = run_server_in_thread(TEST_DB, PORT)
    conn = HTTPConnection("localhost", PORT)

    yield conn

    conn.close()
    httpd.shutdown()
    thread.join()


def test_status(server):
    server.request("GET", "/status")
    response = server.getresponse()
    assert response.status == 200
    data = json.load(response)
    assert data == {"status": "ok"}
