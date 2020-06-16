from flask_sqlalchmey as SQLAlchemy

db = SQLAlchemy()

def dbConnect():
    global engine, connection, metaData
    engine = db.create_engine('postgresql://postgres:password@localhost:5432/ebook')
    connection = engine.connect()
    metaData = db.MetaData()
    print('Connected to DB.')