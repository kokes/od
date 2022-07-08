import pytest

from server import API


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    yield API("test", f"sqlite:///{db_path}").test_client()


def test_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.data == b'{"status":"ok"}\n'
