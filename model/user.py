from . import db, red
import random


class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(200))
    location = db.Column(db.String(500))
    website = db.Column(db.String(200))
    tel = db.Column(db.String(11))
    t_create = db.Column(db.TIMESTAMP)
    t_update = db.Column(db.TIMESTAMP)
    t_delete = db.Column(db.TIMESTAMP)

    def __init__(self, username, password, email=None, tel=None):
        self.username = username
        self.email = email
        self.tel = tel
        self.password = password

    @classmethod
    def generate_account_verification_code(cls, account):
        code = "".join(random.sample('0123456789', 6))
        red.set("vcode-%s" % account, code, 300)
        return code

    @classmethod
    def check_account_verification_code(cls, account, code):
        c = red.get("vcode-%s" % account)
        if c == code:
            return True
        return False

    def create_new_account(self):
        db.session.add(self)
        db.session.commit()