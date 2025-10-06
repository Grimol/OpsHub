from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.db.enums import TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: str | None = None
    priority: TicketPriority = TicketPriority.med
    status: TicketStatus = TicketStatus.open
    project_id: int
    assignee_id: int | None = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    assignee_id: int | None = None


class TicketRead(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
