from datetime import datetime

from pydantic import BaseModel, Field


class TaskDocument(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    title: str
    description: str | None = None
    completed: bool = False
    owner_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
