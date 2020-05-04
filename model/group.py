from . import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    is_all = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, name, is_all, user_id, t_create, t_update, t_delete):
        self.name = name
        self.is_all = is_all
        self.user_id = user_id
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete


class GroupChattingRecord(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    context = db.Column(db.Text, nullable=False)
    t_create = db.Column(db.TIMESTAMP)

    def __init__(self, username, email, t_create):
        self.username = username
        self.email = email
        self.t_create = t_create


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
