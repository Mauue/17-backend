from . import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, name, user_id, t_create, t_update, t_delete):
        self.name = name
        self.user_id = user_id
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete

