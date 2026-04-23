from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


@dataclass
class Book:
    id: UUID
    title: str
    author: str
    description: str
    status: BookStatus
    year: int