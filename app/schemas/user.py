from pydantic import BaseModel, ConfigDict, EmailStr

from app.db.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.viewer
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: UserRole


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
