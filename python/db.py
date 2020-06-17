from flask_sqlalchemy import SQLAlchemy

def dbConnect():
    global engine, connection, metaData
    engine = db.create_engine('postgresql://postgres:password@localhost:5432/ebook')
    connection = engine.connect()
    metaData = db.MetaData()
    print('Connected to PostgreSQL DB.')

db = SQLAlchemy()