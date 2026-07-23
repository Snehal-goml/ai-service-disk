"""
Tests for endpoint: POST /tickets/{ticket_id}/close  (Close ticket)
"""
import pytest


def _create_open_ticket(client):
    r = client.post("/tickets", json={"title": "Open ticket", "status": "open"})
    return r.json()["id"]


def _create_closed_ticket(client):
    tid = _create_open_ticket(client)
    client.put(f"/tickets/{tid}", json={"status": "closed"})
    return tid


def test_close_open_ticket_200(client):
    tid = _create_open_ticket(client)
    r = client.post(f"/tickets/{tid}/close")
    assert r.status_code == 200


def test_close_open_ticket_returns_closed(client):
    tid = _create_open_ticket(client)
    r = client.post(f"/tickets/{tid}/close")
    assert r.json()["status"] == "closed"


def test_close_already_closed_409(client):
    tid = _create_closed_ticket(client)
    r = client.post(f"/tickets/{tid}/close")
    assert r.status_code == 409


def test_close_already_closed_error_body(client):
    tid = _create_closed_ticket(client)
    r = client.post(f"/tickets/{tid}/close")
    data = r.json()
    assert data["error"] == "closed_ticket"
    assert data["id"] == tid


def test_close_nonexistent_ticket_404(client):
    r = client.post("/tickets/nonexistent-id/close")
    assert r.status_code == 404


def test_close_nonexistent_error_body(client):
    r = client.post("/tickets/nonexistent-id/close")
    data = r.json()
    assert data["error"] == "ticket_not_found"
    assert data["id"] == "nonexistent-id"


def test_close_updates_updated_at(client):
    tid = _create_open_ticket(client)
    r1 = client.get(f"/tickets/{tid}")
    before = r1.json()["updated_at"]
    client.post(f"/tickets/{tid}/close")
    r2 = client.get(f"/tickets/{tid}")
    assert r2.json()["updated_at"] != before