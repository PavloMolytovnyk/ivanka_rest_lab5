from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str
    status: BookStatus
    year: int


class BookResponse(BookCreate):
    id: UUID