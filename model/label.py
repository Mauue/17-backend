from . import db


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, project_id, name):
        self.project_id = project_id
        self.name = name

