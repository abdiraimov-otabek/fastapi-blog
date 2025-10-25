import datetime
import uuid
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import bleach


ALLOWED_TAGS = [
    "p",
    "b",
    "i",
    "u",
    "em",
    "strong",
    "a",
    "ul",
    "ol",
    "li",
    "blockquote",
    "br",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "code",
]
ALLOWED_ATTRS = {"a": ["href", "title"]}


def sanitize_html(value: str) -> str:
    return bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)


class PostOut(BaseModel):
    id: uuid.UUID
    title: str
    short_description: str
    content: str
    is_published: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    @field_validator("content", mode="before")
    def sanitize_content(cls, v: str):
        return sanitize_html(v)

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    short_description: str = Field(..., max_length=300)
    content: str
    is_published: bool = False

    @field_validator("content", mode="before")
    def sanitize_content(cls, v: str):
        return sanitize_html(v)


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    short_description: Optional[str] = Field(None, max_length=300)
    content: Optional[str] = None
    is_published: Optional[bool] = None

    @field_validator("content", mode="before")
    def sanitize_content(cls, v: Optional[str]):
        return sanitize_html(v) if v else v
