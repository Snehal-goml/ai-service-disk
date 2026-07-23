
import pytest


def test_home_returns_200(client):
    r = client.get("/")
    assert r.status_code == 200


def test_home_returns_app_name(client):
    r = client.get("/")
    data = r.json()
    assert "message" in data


def test_home_message_is_string(client):
    r = client.get("/")
    assert isinstance(r.json()["message"], str)


def test_home_non_empty_message(client):
    r = client.get("/")
    assert len(r.json()["message"]) > 0

def test_home_has_x_response_time_header(client):
    r = client.get("/")
    assert "X-Response-Time" in r.headers


def test_home_x_response_time_format(client):
    r = client.get("/")
    header = r.headers["X-Response-Time"]
    assert header.endswith("ms")
    assert header[:-2].isdigit()


def test_home_response_is_json(client):
    r = client.get("/")
    assert r.headers["content-type"].startswith("application/json")