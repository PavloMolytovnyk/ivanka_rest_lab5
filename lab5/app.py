from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from resources.book import BookListResource, BookResource

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app)

api.add_resource(BookListResource, "/books")
api.add_resource(BookResource, "/books/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)