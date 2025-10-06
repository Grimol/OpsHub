import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    agent = "agent"
    viewer = "viewer"


class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"


class TicketPriority(str, enum.Enum):
    low = "low"
    med = "med"
    high = "high"


class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"
