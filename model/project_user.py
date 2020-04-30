from . import db


class ProjectUser(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.SmallInteger, nullable=False)
    t_attend = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, user_id, identity, t_attend, t_delete):
        self.user_id = user_id
        self.identity = identity
        self.t_attend = t_attend
        self.t_delete = t_delete

