from . import db


class TaskUser(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    t_attend = db.Column(db.TIMESTAMP)

    def __init__(self, task_id, user_id, t_attend):
        self.task_id = task_id
        self.user_id = user_id
        self.t_attend = t_attend

