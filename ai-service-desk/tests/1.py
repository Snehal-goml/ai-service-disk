"""
Tests for endpoint: GET /
"""
import pytest


def test_home_returns_200(client):
    """Verify the home endpoint returns status 200."""
    r = client.get("/")
    assert r.status_code == 200


def test_home_returns_app_name(client):
    """Verify the response contains the 'message' key."""
    r = client.get("/")
    data = r.json()
    assert "message" in data


def test_home_message_is_string(client):
    """Verify the message value is a string."""
    r = client.get("/")
    assert isinstance(r.json()["message"], str)


def test_home_non_empty_message(client):
    """Verify the message is not empty."""
    r = client.get("/")
    assert len(r.json()["message"]) > 0


def test_home_has_x_response_time_header(client):
    """Verify the X-Response-Time header is present."""
    r = client.get("/")
    assert "X-Response-Time" in r.headers


def test_home_x_response_time_format(client):
    """Verify the X-Response-Time header ends with 'ms' and has a numeric prefix."""
    r = client.get("/")
    header = r.headers["X-Response-Time"]
    assert header.endswith("ms")
    assert header[:-2].isdigit()


def test_home_response_is_json(client):
    """Verify the response content type is JSON."""
    r = client.get("/")
    assert r.headers["content-type"].startswith("application/json")