from . import db


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    project_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(500))
    label = db.Column(db.Text)
    t_remind = db.Column(db.TIMESTAMP)
    t_set = db.Column(db.TIMESTAMP)
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    t_delete = db.Column(db.TIMESTAMP, default=None)

    def __init__(self, content, user_id, t_set):
        self.content = content
        self.user_id = user_id
        self.t_set = t_set

