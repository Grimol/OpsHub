from pydantic import BaseModel, ConfigDict
from app.db.models import ProjectStatus

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    status: ProjectStatus = ProjectStatus.active
    owner_id: int | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    owner_id: int | None = None

class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    status: ProjectStatus
    owner_id: int | None
