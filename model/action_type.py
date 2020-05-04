from . import db


class ActionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, name, content):
        self.name = name
        self.content = content

