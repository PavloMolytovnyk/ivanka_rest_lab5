import pytest
from httpx import AsyncClient, ASGITransport  # Додайте імпорт ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_create_and_get_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        payload = {
            "title": "Test Book",
            "author": "Author 1",
            "description": "desc",
            "status": "available",
            "year": 2024
        }

        res = await ac.post("/books", json=payload)
        assert res.status_code == 201
        book = res.json()

        res2 = await ac.get(f"/books/{book['id']}")
        assert res2.status_code == 200
        assert res2.json()["title"] == "Test Book"


@pytest.mark.anyio
async def test_delete_idempotent():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        res = await ac.delete("/books/00000000-0000-0000-0000-000000000000")
        assert res.status_code == 204