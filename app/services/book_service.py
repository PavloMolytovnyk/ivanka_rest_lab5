from uuid import uuid4, UUID
from typing import List, Optional

from app.schemas.book import BookCreate
from app.models.book import Book, BookStatus
from app.repository.book_repository import BookRepository


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def get_books(
        self,
        author: Optional[str] = None,
        status: Optional[BookStatus] = None,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ) -> List[Book]:

        books = await self.repo.get_all()

        if author:
            books = [b for b in books if b.author == author]

        if status:
            books = [b for b in books if b.status == status]

        reverse = order == "desc"

        if sort_by == "title":
            books.sort(key=lambda x: x.title, reverse=reverse)
        elif sort_by == "year":
            books.sort(key=lambda x: x.year, reverse=reverse)

        return books

    async def get_by_id(self, book_id: UUID) -> Optional[Book]:
        return await self.repo.get_by_id(book_id)

    async def create(self, data: BookCreate) -> Book:
        book = Book(
            id=uuid4(),
            title=data.title,
            author=data.author,
            description=data.description,
            status=data.status,
            year=data.year
        )
        return await self.repo.add(book)

    async def delete(self, book_id: UUID) -> bool:
        return await self.repo.delete(book_id)