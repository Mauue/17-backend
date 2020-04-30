from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(200))
    location = db.Column(db.String(500))
    website = db.Column(db.String(200))
    tel = db.Column(db.String(11))
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, username, email, password, photo, location, website, tel, t_create, t_update, t_delete):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo
        self.location = location
        self.website = website
        self.tel = tel
        self.t_create = t_create
        self.t_update = t_update
        self.t_delete = t_delete
