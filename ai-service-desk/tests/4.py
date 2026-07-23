"""
Tests for endpoints: GET, PUT, DELETE /tickets/{ticket_id}
"""
import pytest


def _create_ticket(client):
    r = client.post("/tickets", json={"title": "Test ticket"})
    return r.json()["id"]


def test_get_ticket_returns_200(client):
    tid = _create_ticket(client)
    r = client.get(f"/tickets/{tid}")
    assert r.status_code == 200


def test_get_ticket_returns_correct_id(client):
    tid = _create_ticket(client)
    r = client.get(f"/tickets/{tid}")
    assert r.json()["id"] == tid


def test_get_ticket_not_found_404(client):
    r = client.get("/tickets/nonexistent-id")
    assert r.status_code == 404


def test_get_ticket_not_found_error_body(client):
    r = client.get("/tickets/nonexistent-id")
    data = r.json()
    assert data["error"] == "ticket_not_found"
    assert data["id"] == "nonexistent-id"


def test_update_ticket_title(client):
    tid = _create_ticket(client)
    r = client.put(f"/tickets/{tid}", json={"title": "Updated title"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated title"


def test_update_ticket_not_found_404(client):
    r = client.put("/tickets/nonexistent-id", json={"title": "New title"})
    assert r.status_code == 404


def test_delete_ticket_returns_204(client):
    tid = _create_ticket(client)
    r = client.delete(f"/tickets/{tid}")
    assert r.status_code == 204


def test_delete_ticket_not_found_404(client):
    r = client.delete("/tickets/nonexistent-id")
    assert r.status_code == 404


def test_delete_ticket_actually_deletes(client):
    tid = _create_ticket(client)
    client.delete(f"/tickets/{tid}")
    r = client.get(f"/tickets/{tid}")
    assert r.status_code == 404


def test_get_ticket_details(client):
    tid = _create_ticket(client)
    r = client.get(f"/tickets/{tid}")
    data = r.json()
    assert all(k in data for k in ("id", "title", "priority", "status",
                                    "created_at", "updated_at"))