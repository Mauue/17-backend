from . import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP)
    type_id = db.Column(db.SmallInteger)
    content = db.Column(db.String(200))

    def __init__(self, user_id, project_id, time, type_id, content):
        self.user_id = user_id
        self.project_id = project_id
        self.time = time
        self.type_id = type_id
        self.content = content

