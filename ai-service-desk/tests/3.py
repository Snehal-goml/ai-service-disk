"""
Tests for endpoints: POST /tickets  (Create ticket)
"""
import pytest


def test_create_ticket_returns_201(client):
    r = client.post("/tickets", json={"title": "Test ticket"})
    assert r.status_code == 201


def test_create_ticket_returns_ticket(client):
    r = client.post("/tickets", json={"title": "Test ticket"})
    data = r.json()
    assert "id" in data
    assert data["title"] == "Test ticket"


def test_create_ticket_default_priority(client):
    r = client.post("/tickets", json={"title": "Test ticket"})
    assert r.json()["priority"] == "medium"


def test_create_ticket_default_status(client):
    r = client.post("/tickets", json={"title": "Test ticket"})
    assert r.json()["status"] == "open"


def test_create_ticket_with_assignee(client):
    r = client.post("/tickets", json={
        "title": "Assigned ticket",
        "assignee_email": "user@example.com"
    })
    assert r.json()["assignee_email"] == "user@example.com"


def test_create_ticket_missing_title_422(client):
    r = client.post("/tickets", json={})
    assert r.status_code == 422


def test_create_ticket_has_id_fields(client):
    r = client.post("/tickets", json={"title": "Complete ticket"})
    data = r.json()
    assert "created_at" in data
    assert "updated_at" in data