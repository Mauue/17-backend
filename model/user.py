from . import db, red
from .oss import oss
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
    t_create = db.Column(db.TIMESTAMP, server_default=db.func.now())
    t_update = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now(),)
    t_delete = db.Column(db.TIMESTAMP, default=None)

    def __init__(self, username, password, email=None, tel=None):
        self.username = username
        self.email = email
        self.tel = tel
        self.password = password

    @staticmethod
    def generate_account_verification_code(account):
        code = "".join(random.sample('0123456789', 6))
        red.set("vcode-%s" % account, code, 300)
        return code

    @staticmethod
    def check_account_verification_code(account, code):
        c = red.get("vcode-%s" % account)
        if c == code:
            return True
        return False

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_phone(phone):
        return User.query.filter_by(tel=phone).first()

    def create_new_account(self):
        db.session.add(self)
        db.session.commit()

    def project_list(self):
        ps = self.projects.all()
        pc = self.project_create
        return [{"id": p.id, "name": p.name, "identity": "member"} for p in ps] + \
                [{"id": p.id, "name": p.name, "identity": "originator"} for p in pc]

    def update_info(self, name, website, location):
        self.username = name
        self.website = website
        self.location = location
        db.session.add(self)
        db.session.commit()

    def upload_photo(self, file, file_extension):
        success, path = oss.upload_photo(file=file, file_extension=file_extension, old_file=self.photo)
        if success:
            self.photo = path
            db.session.add(self)
            db.session.commit()
            return True
        return False
