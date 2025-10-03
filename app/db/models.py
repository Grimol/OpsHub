from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Integer, Boolean, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    agent = "agent"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.viewer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    tickets_assigned: Mapped[list["Ticket"]] = relationship(back_populates="assignee")

class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.active)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    owner: Mapped["User"] = relationship(back_populates="projects")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="project")

class TicketPriority(str, enum.Enum):
    low = "low"
    med = "med"
    high = "high"

class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.med)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.open)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    project: Mapped["Project"] = relationship(back_populates="tickets")
    assignee: Mapped["User"] = relationship(back_populates="tickets_assigned")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(255))
    target_type: Mapped[str] = mapped_column(String(50))
    target_id: Mapped[int | None]
    payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
