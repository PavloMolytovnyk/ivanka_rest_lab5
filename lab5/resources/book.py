from flask_restful import Resource, reqparse
from flask import request
from models.book import books

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Title is required")
parser.add_argument("author", type=str, required=True, help="Author is required")
parser.add_argument("year", type=int, required=True, help="Year must be an integer")


class BookListResource(Resource):
    def get(self):
        """
        Get all books (with filters + pagination)
        ---
        tags:
          - Books
        definitions:
          Book:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
              year:
                type: integer
            example:
              id: 1
              title: "You Don't Know JS: Scope & Closures"
              author: "Kyle Simpson"
              year: 2014
          BookListResponse:
            type: object
            properties:
              filters:
                type: object
                properties:
                  author:
                    type: string
                  title:
                    type: string
                  year:
                    type: integer
              count:
                type: integer
              result:
                type: array
                items:
                  $ref: '#/definitions/Book'
        parameters:
          - name: author
            in: query
            type: string
            description: Filter by author name
          - name: title
            in: query
            type: string
            description: Filter by book title
          - name: year
            in: query
            type: integer
            description: Filter by publication year
          - name: limit
            in: query
            type: integer
            default: 10
          - name: offset
            in: query
            type: integer
            default: 0
        responses:
          200:
            description: List of books
            schema:
              $ref: '#/definitions/BookListResponse'
          400:
            description: Invalid pagination parameters
        """
        author = request.args.get("author")
        title = request.args.get("title")
        year = request.args.get("year")

        try:
            limit = int(request.args.get("limit", 10))
            offset = int(request.args.get("offset", 0))
        except ValueError:
            return {"message": "limit and offset must be integers"}, 400

        result = books.copy()

        if author:
            result = [b for b in result if author.lower() in b["author"].lower()]

        if title:
            result = [b for b in result if title.lower() in b["title"].lower()]

        if year:
            try:
                year = int(year)
            except ValueError:
                return {"message": "Year must be an integer"}, 400
            result = [b for b in result if b["year"] == year]

        total_count = len(result)
        result = result[offset: offset + limit]

        return {
            "filters": {
                "author": author,
                "title": title,
                "year": year
            },
            "count": total_count,
            "result": result
        }, 200

    def post(self):
        """
        Create a book
        ---
        tags:
          - Books
        definitions:
          BookInput:
            type: object
            required:
              - title
              - author
              - year
            properties:
              title:
                type: string
              author:
                type: string
              year:
                type: integer
            example:
              title: "Fluent Python"
              author: "Luciano Ramalho"
              year: 2015
          BookCreateResponse:
            type: object
            properties:
              message:
                type: string
              input:
                $ref: '#/definitions/BookInput'
              output:
                $ref: '#/definitions/Book'
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/BookInput'
        responses:
          201:
            description: Book created successfully
            schema:
              $ref: '#/definitions/BookCreateResponse'
          400:
            description: Invalid input
        """
        data = parser.parse_args()

        new_id = max([b["id"] for b in books], default=0) + 1

        book = {
            "id": new_id,
            "title": data["title"],
            "author": data["author"],
            "year": data["year"]
        }

        books.append(book)

        return {
            "message": "Book created successfully",
            "input": data,
            "output": book
        }, 201


class BookResource(Resource):
    def get(self, book_id):
        """
        Get book by ID
        ---
        tags:
          - Books
        definitions:
          BookSingleResponse:
            type: object
            properties:
              requested_id:
                type: integer
              found:
                type: boolean
              book:
                $ref: '#/definitions/Book'
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book found
            schema:
              $ref: '#/definitions/BookSingleResponse'
          404:
            description: Book not found
        """
        for book in books:
            if book["id"] == book_id:
                return {
                    "requested_id": book_id,
                    "found": True,
                    "book": book
                }, 200

        return {
            "requested_id": book_id,
            "found": False,
            "message": "Book not found"
        }, 404

    def delete(self, book_id):
        """
        Delete book
        ---
        tags:
          - Books
        definitions:
          BookDeleteResponse:
            type: object
            properties:
              deleted_id:
                type: integer
              success:
                type: boolean
              remaining_books:
                type: integer
            example:
              deleted_id: 1
              success: true
              remaining_books: 5
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book successfully deleted
            schema:
              $ref: '#/definitions/BookDeleteResponse'
          404:
            description: Book not found
        """
        global books

        initial_len = len(books)
        books = [b for b in books if b["id"] != book_id]

        if len(books) == initial_len:
            return {
                "deleted_id": book_id,
                "success": False,
                "message": "Book not found"
            }, 404

        return {
            "deleted_id": book_id,
            "success": True,
            "remaining_books": len(books)
        }, 200