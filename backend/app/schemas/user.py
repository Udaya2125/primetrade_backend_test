from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8)


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    role: str = "user"
    is_active: bool = True
    created_at: datetime | None = None


class UserInDB(UserPublic):
    hashed_password: str
    updated_at: datetime | None = None
