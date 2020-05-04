from . import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    size = db.Column(db.Float)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, user_id, name, location, size, t_create, t_update, t_delete):
        self.user_id = user_id
        self.name = name
        self.location = location
        self.size = size
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete

