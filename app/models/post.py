import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    content: str  # your HTML or markdown
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    is_published: bool = Field(default=True)
