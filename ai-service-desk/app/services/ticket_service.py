from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ClosedTicketError, TicketNotFoundError
from app.models.ticket import Ticket


class TicketService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict[str, Any]) -> Ticket:
        ticket = Ticket(**data)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> list[Ticket]:
        stmt = select(Ticket)
        if status:
            stmt = stmt.where(Ticket.status == status)
        if priority:
            stmt = stmt.where(Ticket.priority == priority)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, ticket_id: str) -> Ticket | None:
        result = await self.session.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()

    async def update(self, ticket_id: str, data: dict[str, Any]) -> Ticket:
        ticket = await self.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)

        # Business rule: closed tickets cannot be reopened
        if ticket.status == "closed" and data.get("status") == "open":
            raise ClosedTicketError(ticket_id)

        for key, value in data.items():
            setattr(ticket, key, value)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def close(self, ticket_id: str) -> Ticket:
        ticket = await self.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        if ticket.status == "closed":
            raise ClosedTicketError(ticket_id)
        ticket.status = "closed"
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def delete(self, ticket_id: str) -> None:
        ticket = await self.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        await self.session.delete(ticket)
        await self.session.commit()
