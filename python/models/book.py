from db import db
from datetime import datetime

class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(), )
    book_description = db.Column(db.String())
    book_genre = db.Column(db.String())
    book_creation = db.Column(db.DateTime)
    book_update = db.Column(db.DateTime)

    chapters = db.relationship('ChapterModel', lazy='dynamic')

    def __init__(self, book_title, book_description, book_genre, book_creation=datetime.now(), book_update=datetime.now()):
        self.book_title = book_title
        self.book_description = book_description
        self.book_genre = book_genre
        self.book_creation = book_creation
        self.book_update = book_update

    def json(self):
        return {"book_id": self.book_id, "book_title": self.book_title, 
            "book_description": self.book_description, "book_genre": self.book_genre, 
            "book_creation": self.book_creation.strftime('%Y-%m-%d %X'), "book_update": self.book_update.strftime('%Y-%m-%d %X'),
            'chapters': [chapter.json() for chapter in self.chapters.all()]}

    def saveToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findById(cls, book_id):
        # SELECT * FROM books WHERE book_id = book_id LIMIT 1
        return cls.query.filter_by(book_id=book_id)

    @classmethod
    def findByName(cls, book_title):
        # SELECT * FROM books WHERE book_title = book_title
        return cls.query.filter_by(book_title=book_title)

    @classmethod
    def queryAll(cls):
        # Return non-chapter information from books (think about this)
        return cls.query.all()