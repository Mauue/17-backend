from . import db
from model.im import IM


class Group(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    im_id = db.Column(db.String(50))
    name = db.Column(db.String(20), nullable=False)
    is_all = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)

    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    t_delete = db.Column(db.TIMESTAMP, default=None)

    project = db.relationship("Project", backref="groups")
    owner = db.relationship("User", backref="own_group")

    def __init__(self, name, is_all, user_id, project_id):
        self.name = name
        self.is_all = is_all
        self.user_id = user_id
        self.project_id = project_id

    @staticmethod
    def new(name, is_all, user, project_id):
        g = Group(name=name, is_all=is_all, user_id=user.id, project_id=project_id)
        db.session.add(g)
        db.session.commit()
        g.im_id = "@b17#group{gid}".format(gid=g.id)
        db.session.add(g)
        db.session.commit()
        resp = IM.create_group(user=user, gid=g.id, name=name, pid=project_id)
        if resp is None:
            return g
        print("error:", resp)
        db.session.delete(g)
        db.session.commit()
        return None

    def add(self, user):
        resp = IM.joinGroup(gid=self.im_id, pid=self.project_id, user=user)
        return resp

    def remove(self, user):
        resp = IM.leaveGroup(gid=self.im_id, pid=self.project_id, uid=user.id)
        resp = IM.delete_account(project_id=self.project_id, user_id=user.id)
        return resp

    def delete(self):
        gid = self.im_id
        db.session.delete(self)
        db.session.commit()
        IM.destroy_group(gid)

    @staticmethod
    def get_by_project_id(project_id):
        g = Group.query.filter_by(project_id=project_id).all()
        return g


# class GroupChattingRecord(db.Model):
#     group_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     context = db.Column(db.Text, nullable=False)
#     t_create = db.Column(db.TIMESTAMP)
#
#     def __init__(self, username, email, t_create):
#         self.username = username
#         self.email = email
#         self.t_create = t_create
#
#
# class GroupUser(db.Model):
#     group_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     project_id = db.Column(db.Integer, nullable=False)
#     t_attend = db.Column(db.TIMESTAMP)
#     t_delete = db.Column(db.TIMESTAMP)
#
#     def __init__(self, group_id, user_id, project_id, t_attend, t_delete):
#         self.group_id = group_id
#         self.user_id = user_id
#         self.project_id = project_id
#         self.t_attend = t_attend
#         self.t_delete = t_delete

