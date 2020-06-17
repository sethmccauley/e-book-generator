from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.book import BookModel

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
        book = BookModel.findById(book_id)
        # Return whole book for displaying chapters/descriptions etc in viewer
        if book:
            return book.json(), 200
        return {"message": "Book now found."}, 404

    def post(self):
        # Fetch json data sent will not error by default when not present or poorly formatted.
        data = Book.parser.parse_args()
        # Database will auto-increment for us as well as populate create/update times.
        book = BookModel(data["book_title"], data["book_description"], data["book_genre"])
        try:
            book.saveToDb()
        except:
            return {"message": "An error occured creating the book."}, 500
        # Response
        return book.json(), 201

    def delete(self, book_id):
        book = BookModel.findById(book_id)
        if book:
            book.deleteFromDb()
        return {"message": "Book Deleted"}

    def put(self, book_id):
        data = Book.parser.parse_args()
        book = BookModel.findById(book_id)

        if book is None:
            book = BookModel(data['book_title'], data['book_description'], data['book_genre'])
        else:
            book.book_title = data['book_title']
            book.book_description = data['book_description']
            book.book_genre = data['book_genre']
            # Updated TimeStamp
        book.saveToDb()
        return book.json()

class BookList(Resource):
    def get(self):
        connection = sqlite3.connect()
        cursor = connection.cursor()
        query = "SELECT * FROM books"
        result = cursor.execute(query)
        cursor.commit()
        cursor.close()

        return {"books": result}