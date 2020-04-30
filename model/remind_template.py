from . import db


class RemindTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, content):
        self.content = content

