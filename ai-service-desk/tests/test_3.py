
import pytest
from app.services.ticket_service import TicketService


# ── Create ticket ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_ticket_returns_ticket_object(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Test ticket"})
    assert ticket is not None


@pytest.mark.asyncio
async def test_create_ticket_has_generated_id(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Test ticket"})
    assert ticket.id is not None
    assert isinstance(ticket.id, str)
    assert len(ticket.id) > 0


@pytest.mark.asyncio
async def test_create_ticket_title_matches_input(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "My First Ticket"})
    assert ticket.title == "My First Ticket"


@pytest.mark.asyncio
async def test_create_ticket_default_priority_is_medium(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Priority check"})
    assert ticket.priority == "medium"


@pytest.mark.asyncio
async def test_create_ticket_default_status_is_open(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Status check"})
    assert ticket.status == "open"


@pytest.mark.asyncio
async def test_create_ticket_has_created_at_timestamp(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Timestamp test"})
    assert ticket.created_at is not None


@pytest.mark.asyncio
async def test_create_ticket_has_updated_at_timestamp(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Updated timestamp"})
    assert ticket.updated_at is not None


@pytest.mark.asyncio
async def test_create_ticket_with_assignee_email(ticket_service: TicketService):
    ticket = await ticket_service.create({
        "title": "Assigned Ticket",
        "assignee_email": "dev@example.com",
    })
    assert ticket.assignee_email == "dev@example.com"


@pytest.mark.asyncio
async def test_create_ticket_without_assignee_defaults_to_none(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "No Assignee"})
    assert ticket.assignee_email is None