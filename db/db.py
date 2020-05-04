from flask_sqlalchemy import SQLAlchemy
import threading


class DB(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.client = SQLAlchemy()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with DB._instance_lock:
                if not hasattr(cls, '_instance'):
                    DB._instance = super().__new__(cls)

        return DB._instance

