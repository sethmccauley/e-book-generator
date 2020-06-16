from flask_cors import CORS
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
CORS(app, suppots_credentials=True)
api = Api(app)

books = []

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_title',
        type=str,
        required=True
    )
    parser.add_argument('book_description',
        type=str,
        required=False
    )
    parser.add_argument('book_genre',
        type=str,
        required=False
    )
    
    def get(self, book_id):
        book = next(filter(lambda x: x['book_id'] == book_id, books), None)
        # Return whole book for displaying chapters/descriptions etc in viewer
        return {book_id: book}, 200 if book else 404

    def post(self):
        # Fetch json data sent will not error by default when not present or poorly formatted.
        data = Book.parser.parse_args()
        # Database will auto-increment for us as well as populate create/update times.
        count = len(books) + 1
        book = {"book_id": count, "book_title": data["book_title"], "book_description": data["book_description"], "book_genre": data["book_genre"]}
        books.append(book)
        # Response
        return book, 201

    def delete(self, book_id):
        global books
        found = False
        if next(filter(lambda x: x["book_id"] == book_id, books)):
            found = True
        books = list(filter(lambda x: x["book_id"] != book_id, books))
        return {book_id: found}, 200 if found else 404

    def put(self, book_id):
        data = Book.parser.parse_args()
        book = next(filter(lambda x: x["book_id"] == book_id, books), None)
        if book is None:
            count = len(books) + 1
            book = {"book_id": count, "book_title": data["book_title"], "book_description": data["book_description"], "book_genre": data["book_genre"]}
            books.append(book)
        else:
            book.update(data)
        return book, 200


class BookList(Resource):
    def get(self):
        return books

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>', '/books/')

if __name__ == '__main__':
    app.run(port=5000,debug=True)