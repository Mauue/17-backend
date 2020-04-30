from . import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    remarks = db.Column(db.Text)
    completion = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer)
    t_begin = db.Column(db.TIMESTAMP)
    t_end = db.Column(db.TIMESTAMP)
    priority = db.Column(db.SmallInteger)
    warn = db.Column(db.SmallInteger)
    label = db.Column(db.Text)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, name, remarks, completion, user_id, t_begin, t_end, priority, warn, label, t_create, t_update, t_delete):
        self.name = name
        self.remarks = remarks
        self.completion = completion
        self.user_id = user_id
        self.t_begin = t_begin
        self.t_end = t_end
        self.priority = priority
        self.warn = warn
        self.label = label
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete

