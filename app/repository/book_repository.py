from typing import List, Optional
from uuid import UUID

from app.models.book import Book


class BookRepository:
    def __init__(self):
        self._books: List[Book] = []

    async def get_all(self) -> List[Book]:
        return self._books

    async def get_by_id(self, book_id: UUID) -> Optional[Book]:
        return next((b for b in self._books if b.id == book_id), None)

    async def add(self, book: Book) -> Book:
        self._books.append(book)
        return book

    async def delete(self, book_id: UUID) -> bool:
        for i, b in enumerate(self._books):
            if b.id == book_id:
                del self._books[i]
                return True
        return False