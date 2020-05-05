from lib.code import code_list
from flask import session, g
from werkzeug.security import check_password_hash, generate_password_hash
from model.user import User
from db import db
import re


def _save_session(user_id):
    session["user"] = user_id


def get_login_user():
    user_id = session.get("user")
    try:
        user_id = int(user_id)
        user = User.get_user_by_id(user_id)
    except TypeError:
        user = None
    if user is None:
        g.user = None
    else:
        g.user = user


def register_by_email(email, password, username):
    result = re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email)
    if result is None:
        return code_list.EmailFormatWrong

    user = User.get_user_by_email(email)
    if user:
        return code_list.EmailExists

    user = User.new(email=email, password=generate_password_hash(password), username=username)
    return code_list.Success


def register_by_phone(phone, password, username):
    result = re.match(r"^1[0-9]{10}$", phone)
    if result is None:
        return code_list.PhoneFormatWrong

    user = User.get_user_by_phone(phone)
    if user:
        return code_list.PhoneExists

    user = User.new(tel=phone, password=generate_password_hash(password), username=username)
    return code_list.Success


def login_by_phone(phone, password):
    user = User.query.filter_by(tel=phone).first()
    if user is None:
        return code_list.PhoneNoExists

    if not check_password_hash(user.password, password):
        return code_list.PasswordWrong

    _save_session(user_id=user.id)

    return code_list.Success


def login_by_email(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return code_list.EmailNoExists

    if not check_password_hash(user.password, password):
        return code_list.PasswordWrong

    _save_session(user_id=user.id)

    return code_list.Success


def get_user_info():
    if g.user is None:
        return None
    user = g.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.tel,
        "photo": user.photo,
        "location": user.location,
        "website": user.website
    }


def update_user_info(user, username, location, website):
    user.update(name=username, website=website, location=location)
    return code_list.Success


def upload_photo(user, file, filename):
    extension = filename.split('.')[-1]
    if user.upload_photo(file=file, file_extension=extension):
        return code_list.Success
    return code_list.OtherError

