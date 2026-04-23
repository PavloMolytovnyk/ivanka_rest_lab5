from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from app.schemas.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.repository.book_repository import BookRepository
from app.models.book import BookStatus

router = APIRouter()

repo = BookRepository()
service = BookService(repo)


@router.get("/books", response_model=list[BookResponse])
async def get_books(author: str = None,
                    status: BookStatus = None,
                    sort_by: str = None,
                    order: str = "asc"):
    return await service.get_books(author, status, sort_by, order)


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID):
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate):
    return await service.create(payload)


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await service.delete(book_id)
    return None  