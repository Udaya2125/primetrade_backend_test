from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None


class TaskPublic(BaseModel):
    id: str
    title: str
    description: str | None = None
    completed: bool = False
    owner_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
