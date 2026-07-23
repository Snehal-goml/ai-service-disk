from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import TicketNotFoundError
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", status_code=201, response_model=TicketOut)
async def create_ticket(body: TicketCreate, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    return await service.create(body.model_dump())


@router.get("", response_model=list[TicketOut])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    service = TicketService(db)
    return await service.list_tickets(status=status, priority=priority)


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    ticket = await service.get(ticket_id)
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
async def update_ticket(
    ticket_id: str, body: TicketUpdate, db: AsyncSession = Depends(get_db)
):
    service = TicketService(db)
    return await service.update(ticket_id, body.model_dump(exclude_unset=True))


@router.post("/{ticket_id}/close", response_model=TicketOut)
async def close_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    return await service.close(ticket_id)


@router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    await service.delete(ticket_id)