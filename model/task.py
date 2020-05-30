from datetime import datetime

from . import db

tu = db.Table('task_user',
              db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
              db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
              )


class Task(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.Text)
    finish = db.Column(db.Boolean, default=False)
    t_begin = db.Column(db.TIMESTAMP)
    t_end = db.Column(db.TIMESTAMP)
    priority = db.Column(db.SmallInteger)
    label = db.Column(db.Text, default="")
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    t_delete = db.Column(db.TIMESTAMP, default=None)

    project = db.relationship("Project", backref="tasks")
    originator = db.relationship("User", backref="task_originator")
    participants = db.relationship('User', secondary=tu,
                                   backref=db.backref('tasks', lazy='dynamic'))

    def __init__(self, name, project_id, user_id, remarks=None, t_begin=None, t_end=None,
                 priority=None, label=None):
        self.name = name
        self.user_id = user_id
        self.project_id = project_id
        self.remarks = remarks
        self.t_begin = t_begin
        self.t_end = t_end
        self.priority = priority
        self.label = label

    @staticmethod
    def new(name, project_id, user_id, remarks=None, t_begin=None, t_end=None,
            priority=None, label=None):
        task = Task(name, project_id, user_id, remarks=remarks, t_begin=t_begin, t_end=t_end,
                    priority=priority, label=label)
        db.session.add(task)
        db.session.commit()
        return task

    def update(self, name, remarks=None, t_begin=None, t_end=None,
               priority=None, label=None, finish=False):
        self.name = name
        self.remarks = remarks
        self.t_begin = t_begin
        self.t_end = t_end
        self.priority = priority
        self.label = label
        self.finish = finish
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.t_delete = datetime.now()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_task_by_id(tid):
        task = Task.query.filter_by(id=tid).first()
        if task and task.t_delete is not None:
            return None
        return task

    def add_participant(self, user):
        print(self.participants)
        self.participants.append(user)
        db.session.add(self)
        db.session.commit()

    def remove_participant(self, user):
        self.participants.remove(user)
        db.session.add(self)
        db.session.commit()

    def has_participant(self, user):
        return user in self.participants

    @property
    def link(self):
        return "task:%s" % self.id
