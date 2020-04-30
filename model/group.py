from . import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    is_all = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, name, is_all, user_id, t_create, t_update, t_delete):
        self.name = name
        self.is_all = is_all
        self.user_id = user_id
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete

