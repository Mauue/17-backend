
from . import db
from .action_type import type_list

type_list = type_list


class Action(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    type_name = db.Column(db.String(50), db.ForeignKey('action_type.name'))
    content = db.Column(db.String(200))
    link = db.Column(db.String(200))
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())

    actionType = db.relationship('ActionType')
    project = db.relationship('Project', backref='actions')
    user = db.relationship('User', backref='actions')

    def __init__(self, user_id, project_id, type_name, content, link):
        self.user_id = user_id
        self.project_id = project_id
        self.type_name = type_name
        self.content = content
        self.link = link

    @staticmethod
    def new(user_id, project_id, type_name, content, link=None):
        a = Action(user_id=user_id, project_id=project_id, type_name=type_name,
                   content=content, link=link)
        db.session.add(a)
        db.session.commit()
        return a


class ActionType(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    name = db.Column(db.String(50), primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, name, content):
        self.name = name
        self.content = content

    @staticmethod
    def init_type():
        for t in type_list:
            a = ActionType.query.filter_by(name=t.name).first()
            if a is None:
                a = ActionType(t.name, t.content)
                db.session.add(a)
            else:
                if a.content != t.content:
                    a.content = t.content
                    db.session.add(a)
        db.session.commit()

