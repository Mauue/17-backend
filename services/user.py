from lib.code import code_list
from flask import session
from werkzeug.security import check_password_hash
from model.user import User

def _save_session(user_id):
    session["user"] = user_id


def login_by_email(email, password):
    # User.
    # check_password_hash()
    pass