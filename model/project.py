from . import db

pu = db.Table('project_user',
              db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
              db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
              db.Column('identity', db.SmallInteger, nullable=False, default=0),
              db.Column('t_attend', db.TIMESTAMP, server_default=db.func.now()),
              db.Column('t_delete', db.TIMESTAMP, default=None)
              )


class Project(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now(), )
    t_delete = db.Column(db.TIMESTAMP, default=None)

    originator = db.relationship("User", backref="project_create")
    members = db.relationship('User', secondary=pu,
                              backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def create_new_project(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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
                "username": m.username,
                "id": m.id,
                "identity": "member",
                "photo": m.photo
            })
        return members

    def is_project_member(self, user, is_admin=False):
        if self.user_id == user.id:
            return True
        # TODO 管理员查询出了点问题
        if is_admin:
            return False
        for m in self.members:
            if m.id == user.id:
                return True
        return False

    def is_project_originator(self, user):
        return self.user_id == user.id

    @staticmethod
    def get_project_by_id(project_id):
        project_id = int(project_id)
        return Project.query.filter_by(id=project_id).first()

    def add_member(self, user):
        self.members.append(user)
        db.session.add(self)
        db.session.commit()

    def remove_member(self, user):
        self.members.remove(user)
        db.session.add(self)
        db.session.commit()

    def get_task_list(self):
        l = []
        for task in self.tasks:
            if task.t_delete is not None:
                continue
            l.append({
                "id": task.id,
                "name": task.name,
                "remarks": task.remarks,
                "finish": task.finish,
                "originator": {
                    "id": task.user_id,
                    "username": task.originator.username,
                    "photo": task.originator.photo
                },
                "t_begin": task.t_begin,
                "t_end": task.t_end,
                "priority": task.priority,
                "label": task.label,
                "participants": [{
                    "id": p.id,
                    "username": p.username,
                    "photo": p.photo
                } for p in task.participants]
            })
        return l

    def get_schedule_list(self):
        return [
            {
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
            }
            for s in self.schedules
        ]

    def has_task(self, task):
        if task.t_delete is not None:
            return False
        return task in self.tasks

