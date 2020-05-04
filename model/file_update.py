from . import db


class FileUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    t_update = db.Column(db.TIMESTAMP)

    def __init__(self, file_id, user_id, t_update):
        self.file_id = file_id
        self.user_id = user_id
        self.t_update = t_update

