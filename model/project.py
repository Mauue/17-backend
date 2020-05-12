from datetime import datetime

from . import db


class ProjectUser(db.Model):
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    is_admin = db.Column('is_admin', db.Boolean, default=False)

    project = db.relationship('Project', back_populates='members')
    member = db.relationship('User', back_populates='projects')


class Project(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now(), )
    t_delete = db.Column(db.TIMESTAMP, default=None)

    originator = db.relationship("User", backref="project_create")
    members = db.relationship('ProjectUser', back_populates='project')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    @staticmethod
    def new(name, user_id):
        p = Project(name, user_id)
        db.session.add(p)
        db.session.commit()
        return p

    def delete(self):
        self.t_delete = datetime.now()
        db.session.add(self)
        db.session.commit()

    def get_project_member_list(self):
        members = [
            {
                "username": self.originator.username,
                "id": self.user_id,
                "identity": "originator",
                "photo": self.originator.photo
            }
        ]
        for m in self.members:
            members.append({
                "username": m.member.username,
                "id": m.member.id,
                "identity": "admin" if m.is_admin else "member",
                "photo": m.member.photo
            })
        return members

    def has_member(self, user, is_admin=False):
        if self.user_id == user.id:
            return True

        for m in self.members:
            if m.member.id == user.id and (not is_admin or m.is_admin):
                return True
        return False

    def is_project_originator(self, user):
        return self.user_id == user.id

    @staticmethod
    def get_project_by_id(project_id):
        project_id = int(project_id)
        p = Project.query.filter_by(id=project_id).first()
        if p and p.t_delete is not None:
            return None
        return p

    def add_member(self, user):
        pu = ProjectUser()
        pu.member = user
        self.members.append(pu)
        db.session.add(self)
        db.session.commit()

    def remove_member(self, user):
        for m in self.members:
            if m.member == user:
                db.session.delete(m)
                db.session.commit()

    def get_task_list(self):
        list_ = []
        for task in self.tasks:
            if task.t_delete is not None:
                continue
            list_.append({
                "id": task.id,
                "name": task.name,
                "finish": task.finish
            })
        return list_

    def get_schedule_list(self):
        list_ = []
        for s in self.schedules:
            if s.t_delete is not None:
                continue
            list_.append({
                "id": s.id,
                "content": s.content,
                "remarks": s.remarks,
                "t_set": s.t_set,
                "t_remind": s.t_remind,
                "creator": {
                    "id": s.creator.id,
                    "username": s.creator.username,
                    "photo": s.creator.photo
                },
                "label": s.label
            })
        return list_

    def has_task(self, task):
        if task.t_delete is not None:
            return False
        return task in self.tasks

    def has_schedule(self, schedule):
        if schedule.t_delete is not None:
            return False
        return schedule in self.schedules

    def add_admin(self, user):
        for m in self.members:
            if m.member == user:
                m.is_admin = True
                db.session.add(m)
                db.session.commit()

    def remove_admin(self, user):
        for m in self.members:
            if m.member == user:
                m.is_admin = False
                db.session.add(m)
                db.session.commit()

    @property
    def link(self):
        return "project:%s" % self.id
