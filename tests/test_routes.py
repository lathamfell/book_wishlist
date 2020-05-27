import pytest


@pytest.fixture
def setup():
    setup = {}
    yield setup


def test_index(setup, testapp):
    res = testapp.get("/")
    assert res.status_code == 200
    assert res.json["status"] == "OK"

    res = testapp.get("/index")
    assert res.status_code == 200
    assert res.json["status"] == "OK"
