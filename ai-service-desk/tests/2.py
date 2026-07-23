"""
Tests for endpoint: GET /health
"""
import pytest


def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200


def test_health_returns_status_key(client):
    r = client.get("/health")
    assert "status" in r.json()


def test_health_ok_value(client):
    r = client.get("/health")
    assert r.json()["status"] == "ok"


def test_health_has_x_response_time(client):
    r = client.get("/health")
    assert "X-Response-Time" in r.headers


def test_health_no_db_call(client):
    """Health endpoint should be lightweight."""
    r = client.get("/health")
    assert r.elapsed.total_seconds() < 2


def test_health_response_is_json(client):
    r = client.get("/health")
    assert r.headers["content-type"].startswith("application/json")