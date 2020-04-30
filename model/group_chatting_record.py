from . import db


class GroupChattingRecord(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    context = db.Column(db.Text, nullable=False)
    t_create = db.Column(db.TIMESTAMP)

    def __init__(self, username, email, t_create):
        self.username = username
        self.email = email
        self.t_create = t_create

