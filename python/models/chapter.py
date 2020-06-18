from db import db
from datetime import datetime

class ChapterModel(db.Model):
    __tablename__ = 'chapters'

    chapter_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    chapter_name = db.Column(db.String())
    chapter_description = db.Column(db.String())
    chapter_order = db.Column(db.Integer)
    chapter_creation = db.Column(db.DateTime)
    chapter_update = db.Column(db.DateTime)

    book = db.relationship('BookModel')
    # sections = db.relationship('SectionModel', lazy='dynamic')

    def __init__(self, chapter_name, book_id, chapter_description, chapter_order, chapter_creation=datetime.now(), chapter_update=datetime.now()):
        self.chapter_name = chapter_name
        self.book_id = book_id
        self.chapter_description = chapter_description
        self.chapter_order = chapter_order
        self.chapter_creation = chapter_creation
        self.chapter_update = chapter_update

    def json(self):
        return {"chapter_id": self.chapter_id, "book_id": self.book_id, 
            "chapter_name": self.chapter_name, "chapter_description": self.chapter_description, "chapter_order": self.chapter_order,
            "chapter_creation": self.chapter_creation.strftime('%Y-%m-%d %X'), "chapter_update": self.chapter_update.strftime('%Y-%m-%d %X')
            } #'sections': [section.json() for sections in self.sections.all()]

    def saveToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findById(cls, chapter_id):
        # SELECT * FROM books WHERE chapter_id = chapter_id LIMIT 1
        return cls.query.filter_by(chapter_id=chapter_id).first()

    @classmethod
    def findByName(cls, chapter_name):
        # SELECT * FROM books WHERE chapter_title = chapter_title
        return cls.query.filter_by(chapter_name=chapter_name)

    @classmethod
    def queryAll(cls, book_id):
        # Return all chapters for given book_id
        return cls.query.filter_by(book_id=book_id)