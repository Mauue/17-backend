from . import db


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    user_id = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(500))
    label = db.Column(db.Text)
    t_remind = db.Column(db.TIMESTAMP)
    t_set = db.Column(db.TIMESTAMP)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, content, user_id, remarks, label, t_remind, t_set, t_create, t_update, t_delete):
        self.content = content
        self.user_id = user_id
        self.remarks = remarks
        self.label = label
        self.t_remind = t_remind
        self.t_set = t_set
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete
