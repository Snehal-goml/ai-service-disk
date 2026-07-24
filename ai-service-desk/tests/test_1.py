
import pytest
from app.main import home, health


# ── Home function ──────────────────────────────────────────────────────────────

def test_home_returns_dict():
    res = home()
    assert isinstance(res, dict)


def test_home_returns_message_key():
    res = home()
    assert "message" in res


def test_home_message_is_string():
    res = home()
    assert isinstance(res["message"], str)


def test_home_message_is_non_empty():
    res = home()
    assert len(res["message"]) > 0


def test_home_has_exactly_one_key():
    res = home()
    assert len(res.keys()) == 1


def test_home_message_value_is_not_none():
    res = home()
    assert res["message"] is not None


# ── Health function ────────────────────────────────────────────────────────────

def test_health_returns_dict():
    res = health()
    assert isinstance(res, dict)


def test_health_contains_status_key():
    res = health()
    assert "status" in res


def test_health_status_value_is_ok():
    res = health()
    assert res["status"] == "ok"


def test_health_status_is_string():
    res = health()
    assert isinstance(res["status"], str)


def test_health_has_exactly_one_key():
    res = health()
    assert len(res.keys()) == 1


def test_health_returns_non_empty_dict():
    res = health()
    assert len(res) > 0
