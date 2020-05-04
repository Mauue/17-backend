from . import db


class Schedule(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    remarks = db.Column(db.String(500))
    label = db.Column(db.Text)
    t_remind = db.Column(db.TIMESTAMP)
    t_set = db.Column(db.TIMESTAMP)
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    t_delete = db.Column(db.TIMESTAMP, default=None)

    project = db.relationship("Project", backref="schedules")
    creator = db.relationship("User", backref="schedule_creator")

    def __init__(self, content, project_id, user_id, remarks, t_set, t_remind, label):
        self.content = content
        self.user_id = user_id
        self.project_id = project_id
        self.t_set = t_set
        self.t_remind = t_remind
        self.label = label
        self.remarks = remarks

    def new(self):
        db.session.add(self)
        db.session.commit()

