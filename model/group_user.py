from . import db


class GroupUser(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    t_attend = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, group_id, user_id, project_id, t_attend, t_delete):
        self.group_id = group_id
        self.user_id = user_id
        self.project_id = project_id
        self.t_attend = t_attend
        self.t_delete = t_delete


