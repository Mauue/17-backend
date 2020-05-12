from flask_sqlalchemy import SQLAlchemy
from .db import DB
from .redis import Redis

db = DB().client
red = Redis()


def db_init_app(app):
    db.init_app(app)
    red.init_app(app)

    @app.cli.command('init-db')
    def create_table():
        # db.drop_all()
        db.create_all()
        from model import model_data_init
        model_data_init()
        print("初始化完成")
