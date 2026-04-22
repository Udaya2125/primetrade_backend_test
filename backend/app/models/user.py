from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserDocument(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    email: EmailStr
    full_name: str | None = None
    hashed_password: str
    role: str = "user"
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
