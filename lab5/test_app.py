import pytest
from flask import Flask
from flask_restful import Api

from app import BookListResource, BookResource
import models.book

@pytest.fixture
def app():
    """Створюємо тестовий додаток Flask"""
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Створюємо тестовий клієнт для імітації HTTP-запитів"""
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_db():
    """
    Очищаємо оригінальний список у пам'яті та заповнюємо його тестовими даними.
    """
    models.book.books.clear()  
    models.book.books.extend([ 
        {"id": 1, "title": "Test Book 1", "author": "Author A", "year": 2000},
        {"id": 2, "title": "Test Book 2", "author": "Author B", "year": 2010},
        {"id": 3, "title": "Another Book", "author": "Author A", "year": 2020}
    ])
    yield


def test_get_all_books(client):
    """Тест отримання списку всіх книг"""
    response = client.get('/books')
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 3
    assert len(data["result"]) == 3

def test_get_books_with_filters(client):
    """Тест фільтрації книг за автором"""
    response = client.get('/books?author=Author A')
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2
    assert data["result"][0]["title"] == "Test Book 1"
    assert data["result"][1]["title"] == "Another Book"

def test_get_books_pagination(client):
    """Тест пагінації (ліміт і зсув)"""
    response = client.get('/books?limit=1&offset=1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["result"]) == 1
    assert data["result"][0]["id"] == 2

def test_get_books_invalid_pagination(client):
    """Тест некоректних параметрів пагінації"""
    response = client.get('/books?limit=abc')
    assert response.status_code == 400
    assert "limit and offset must be integers" in response.get_json()["message"]

def test_post_create_book(client):
    """Тест створення нової книги"""
    new_book = {
        "title": "New Python Book",
        "author": "Guido van Rossum",
        "year": 2023
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Book created successfully"
    assert data["output"]["id"] == 4  
    assert data["output"]["title"] == "New Python Book"