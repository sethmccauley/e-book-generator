from db import db
import datetime

class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String())
    book_description = db.Column(db.String())
    book_genre = db.Column(db.String())
    book_creation = db.Column(db.DateTime)
    book_update = db.Column(db.DateTime)

    # chapters = db.relationship('ChapterModel', lazy='dynamic')

    def __init__(self, book_title, book_description, book_genre):
        # self.book_id = book_id
        self.book_title = book_title
        self.book_description = book_description
        self.book_genre = book_genre

    def json(self):
        return {"book_id": self.book_id, "book_title": self.book_title, "book_description": self.book_description, "book_genre": self.book_genre} #'chapters': [chapter.json() for chapters in self.chapters.all()]

    def saveToDb(self):
        # Test if exists, if does, then update book_update, if not update and creation
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findById(cls, book_id):
        # SELECT * FROM books WHERE book_id = book_id LIMIT 1
        return cls.query.filter_by(book_id=book_id).first()

    @classmethod
    def findByName(cls, book_title):
        # SELECT * FROM books WHERE book_title = book_title
        return cls.query.filter_by(book_title=book_title)


# class BookList(db.Model):
#     __init__(self):
#         pass

