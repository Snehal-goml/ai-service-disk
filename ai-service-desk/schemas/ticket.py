from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    priority: str = "medium"
    status: str = "open"
    assignee_email: Optional[str] = None


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assignee_email: Optional[str] = None


class TicketOut(BaseModel):
    id: str
    title: str
    priority: str
    status: str
    assignee_email: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
