
import pytest
from app.core.exceptions import ClosedTicketError, TicketNotFoundError
from app.services.ticket_service import TicketService


# ── Close ticket ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_close_open_ticket_sets_status_to_closed(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Open Ticket", "status": "open"})
    closed = await ticket_service.close(ticket.id)
    assert closed.status == "closed"


@pytest.mark.asyncio
async def test_close_ticket_returns_updated_ticket_object(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Close returns obj"})
    result = await ticket_service.close(ticket.id)
    assert result is not None
    assert result.id == ticket.id


@pytest.mark.asyncio
async def test_close_already_closed_ticket_raises_closed_error(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Double close"})
    await ticket_service.close(ticket.id)
    with pytest.raises(ClosedTicketError) as exc_info:
        await ticket_service.close(ticket.id)
    assert exc_info.value.ticket_id == ticket.id


@pytest.mark.asyncio
async def test_close_nonexistent_ticket_raises_not_found(ticket_service: TicketService):
    with pytest.raises(TicketNotFoundError) as exc_info:
        await ticket_service.close("00000000-0000-0000-0000-000000000000")
    assert exc_info.value.ticket_id == "00000000-0000-0000-0000-000000000000"


@pytest.mark.asyncio
async def test_close_ticket_updated_at_is_refreshed(ticket_service: TicketService):
    ticket = await ticket_service.create({"title": "Timestamp refresh"})
    before = ticket.updated_at
    closed = await ticket_service.close(ticket.id)
    assert closed.updated_at >= before


# ── List tickets ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_tickets_returns_list(ticket_service: TicketService):
    result = await ticket_service.list_tickets()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_list_tickets_filter_by_status_open(ticket_service: TicketService):
    await ticket_service.create({"title": "Open ticket filter", "status": "open"})
    result = await ticket_service.list_tickets(status="open")
    assert all(t.status == "open" for t in result)


@pytest.mark.asyncio
async def test_list_tickets_filter_by_priority_high(ticket_service: TicketService):
    await ticket_service.create({"title": "High priority ticket", "priority": "high"})
    result = await ticket_service.list_tickets(priority="high")
    assert all(t.priority == "high" for t in result)


@pytest.mark.asyncio
async def test_list_tickets_filter_by_status_and_priority_combined(ticket_service: TicketService):
    await ticket_service.create({"title": "Combo filter", "status": "open", "priority": "low"})
    result = await ticket_service.list_tickets(status="open", priority="low")
    assert len(result) >= 1
    assert all(t.status == "open" and t.priority == "low" for t in result)


@pytest.mark.asyncio
async def test_list_closed_tickets_does_not_include_open(ticket_service: TicketService):
    await ticket_service.create({"title": "Will be open", "status": "open"})
    result = await ticket_service.list_tickets(status="closed")
    assert all(t.status == "closed" for t in result)