from flask_sqlalchemy import SQLAlchemy


class DB:
    _instance = None

    def __init__(self, app):
        self.db = SQLAlchemy(app)

    def test(self):
        return id(self)

    @classmethod
    def create_db(cls, app):
        if DB._instance is None:
            DB._instance = DB(app)

    @classmethod
    def instance(cls, app=None):
        if DB._instance is None:
            DB._instance = DB(app)
        return DB._instance

    @classmethod
    def get_db(cls):
        return cls.instance().db


