from . import db


class Remind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP)
    template_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, user_id, project_id, time, template_id, content, t_create, t_update, t_delete):
        self.user_id = user_id
        self.project_id = project_id
        self.time = time
        self.template_id = template_id
        self.content = content
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete

