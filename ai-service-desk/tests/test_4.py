
import pytest
from app.core.exceptions import TicketNotFoundError, ClosedTicketError
from app.services.ticket_service import TicketService


# ── Get ticket ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_ticket_by_id_returns_correct_ticket(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Get test ticket"})
    fetched = await ticket_service.get(ticket.id)
    assert fetched is not None
    assert fetched.id == ticket.id


@pytest.mark.asyncio
async def test_get_nonexistent_ticket_returns_none(ticket_service: TicketService):
    fetched = await ticket_service.get("00000000-0000-0000-0000-000000000000")
    assert fetched is None


@pytest.mark.asyncio
async def test_get_ticket_title_matches(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Title match check"})
    fetched = await ticket_service.get(ticket.id)
    assert fetched.title == "Title match check"


# ── Update ticket ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_ticket_title(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Old Title"})
    updated = await ticket_service.update(ticket.id, {"title": "New Title"})
    assert updated.title == "New Title"


@pytest.mark.asyncio
async def test_update_ticket_priority(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Priority update"})
    updated = await ticket_service.update(ticket.id, {"priority": "high"})
    assert updated.priority == "high"


@pytest.mark.asyncio
async def test_update_nonexistent_ticket_raises_not_found(ticket_service: TicketService):
    with pytest.raises(TicketNotFoundError):
        await ticket_service.update("00000000-0000-0000-0000-000000000000", {"title": "Ghost"})


@pytest.mark.asyncio
async def test_update_closed_ticket_status_to_open_raises_closed_error(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Reopen test", "status": "open"})
    await ticket_service.close(ticket.id)
    with pytest.raises(ClosedTicketError):
        await ticket_service.update(ticket.id, {"status": "open"})


# ── Delete ticket ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_ticket_removes_it(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "To be deleted"})
    await ticket_service.delete(ticket.id)
    fetched = await ticket_service.get(ticket.id)
    assert fetched is None


@pytest.mark.asyncio
async def test_delete_nonexistent_ticket_raises_not_found(ticket_service: TicketService):
    with pytest.raises(TicketNotFoundError):
        await ticket_service.delete("00000000-0000-0000-0000-000000000000")