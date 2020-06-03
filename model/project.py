from datetime import datetime
from model.group import Group
from . import db
from .im import IM


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
    def new(name, user):
        p = Project(name, user.id)
        db.session.add(p)
        db.session.commit()
        Group.new(name=name, is_all=True, project_id=p.id, user=user)
        return p

    def delete(self):
        self.t_delete = datetime.now()
        user_id_list = [m.member.id for m in self.members] + [self.user_id]
        pid = self.id
        groups = self.groups
        db.session.add(self)
        db.session.commit()
        for group in groups:
            group.delete()
        IM.delete_account_batch(pid, user_id_list)

    def get_project_member_list(self):
        members = [
            {
                "username": self.originator.username,
                "id": self.user_id,
                "identity": "originator",
                "photo": self.originator.photo,
                "location": self.originator.location,
                "website": self.originator.website,
                "tel": self.originator.tel
            }
        ]
        for m in self.members:
            members.append({
                "username": m.member.username,
                "id": m.member.id,
                "identity": "admin" if m.is_admin else "member",
                "photo": m.member.photo,
                "location": m.member.location,
                "website": m.member.website,
                "tel": m.member.tel
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
        r = IM.create_account(project_id=self.id, user=user)

    def remove_member(self, user):
        for m in self.members:
            if m.member == user:
                db.session.delete(m)
                db.session.commit()
                r = IM.delete_account(project_id=self.id, user_id=user.id)

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

    def get_remind_by_user(self, user):
        now = datetime.now()
        list_ = []
        for s in self.schedules:
            if s.t_delete is not None or s.t_remind is None or s.t_remind < now:
                continue
            list_.append({
                "type": "schedule:{}".format(s.id),
                "name": s.content,
                "t_remind": s.t_remind,
            })
        for task in self.tasks:
            if task.t_delete is not None or task.t_end is None or task.t_end < now or\
                    task.finish or (task.user_id != user.id and user not in task.participants):
                continue
            list_.append({
                "type": "task:{}".format(task.id),
                "name": task.name,
                "t_remind": task.t_end
            })
        list_.sort(key=lambda item: item["t_remind"])
        return list_

