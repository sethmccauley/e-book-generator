from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.chapter import ChapterModel
from datetime import datetime

class Chapter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('chapter_name',
        type=str,
        required=True,
        help="Chapters require a name."
    )
    parser.add_argument('book_id',
        type=int,
        required=True,
        help="Chapters require a book_id."
    )
    parser.add_argument('chapter_description',
        type=str,
        required=False
    )
    parser.add_argument('chapter_order',
        type=int,
        required=False
    )

    def get(self, chapter_id):
        chapter = ChapterModel.findById(chapter_id)

        if chapter:
            return chapter.json(), 200
        return {"message": "Chapter not found."}, 404

    def post(self):
        data = Chapter.parser.parse_args()

        chapter = ChapterModel(data["chapter_name"], data["book_id"], data["chapter_description"], data["chapter_order"])
        try:
            chapter.chapter_creation = datetime.now()
            chapter.saveToDb()
        except:
            return {"message": "An error occured creating the chapter."}, 500
        return chapter.json(), 201

    def delete(self, chapter_id):
        chapter = ChapterModel.findById(chapter_id)
        if chapter:
            chapter.deleteFromDb()
        return {"message": "Chapter Deleted"}

    def put(self, chapter_id):
        data = Chapter.parser.parse_args()
        chapter = ChapterModel.findById(chapter_id)

        if chapter is None:
            chapter = ChapterModel(data["chapter_name"], data["book_id"], data["chapter_description"], data["chapter_order"])
        else:
            chapter.chapter_name = data['chapter_name']
            chapter.book_id = data['book_id']
            chapter.chapter_description = data['chapter_description']
            chapter.chapter_order = data['chapter_order']
            chapter.chapter_update = datetime.now()

        chapter.saveToDb()
        return chapter.json()

class ChapterList(Resource):
    def get(self, book_id):
        return {"chapters": [chapter.json() for chapter in ChapterModel.queryAll(book_id)]}