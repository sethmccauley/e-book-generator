from flask_cors import CORS
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from db import db

from resources.book import Book, BookList
from resources.chapter import Chapter, ChapterList
# from resources.section import Section, SectionList
# content

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/ebook'
# Saving direct to memory
# appserver.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, supports_credentials=True)
api = Api(app)

api.add_resource(Book, '/book/<int:book_id>', '/book')
api.add_resource(BookList, '/books')
api.add_resource(ChapterList, '/chapters/<int:book_id>')
api.add_resource(Chapter, '/chapter/<int:chapter_id>', '/chapter')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)