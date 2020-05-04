import functools

from flask import Blueprint, request, session, g
from .base import *
from lib.code import code_list
from model.user_form import *
from services import user as service
import re
user_bp = Blueprint('user', __name__, url_prefix='/api')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get("user")
        if user_id is None:
            return response(code_list.NoLogin)
        return view(**kwargs)
    return wrapped_view


def login_user_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        service.get_login_user()
        if g.user is None:
            return response(code_list.NoLogin)
        return view(**kwargs)
    return wrapped_view


@user_bp.route('/user/register', methods=['POST', 'GET'])
@csrf.exempt
def register_user_controllers():
    form = UserRegisterForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))

    # 验证格式
    result = re.match(r"^.{6,20}$", form.password.data)
    if result is None:
        return response(code_list.PasswordFormatWrong)

    result = re.match(r"^[\u4e00-\u9fa5\w]{2,10}$", form.username.data)
    if result is None:
        return response(code_list.UsernameFormatWrong)

    # 注册类型跳转
    if form.account_type.data == "email":
        c = service.register_by_email(form.account.data, form.password.data, form.username.data)
        return response(c)

    if form.account_type.data == "phone":
        c = service.register_by_phone(form.account.data, form.password.data, form.username.data)
        return response(c)

    return response(code_list.ParamsWrong.with_message("未开放注册类型"))


@user_bp.route('/user/login', methods=['POST'])
def login_user():
    form = UserLoginForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))

    if form.account_type.data == "email":
        c = service.login_by_email(form.account.data, form.password.data)
        return response(c)

    if form.account_type.data == "phone":
        c = service.login_by_phone(form.account.data, form.password.data)
        return response(c)
    return response(code_list.ParamsWrong.with_message("未开放登录类型"))


@user_bp.route('/user/logout')
def logout_user():
    session.clear()
    g.user = None
    return response(code_list.Success)


@user_bp.route('/user/info', methods=["POST", "GET"])
@login_user_required
def info_user():
    if request.method == "GET":
        data = service.get_user_info()
        return response(code_list.Success, data)
    else:
        form = UserUpdateInfoForm()
        if not form.validate():
            return response(code_list.ParamsWrong.with_message(form.errors))
        user = g.user
        e = service.update_user_info(user, username=form.username.data, website=form.website.data,
                                     location=form.location.data)
        return response(e)


@user_bp.route('/user/info/photo', methods=["POST"])
@login_user_required
def user_photo():
    form = UserUploadPhotoForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))
    file = form.image.data.stream.read()
    file_length = len(file)
    if file_length > 5 * 1000 * 1000:
        return response(code_list.FileSizeTooBig)

    user = g.user
    e = service.upload_photo(user, file, form.image.data.filename)
    return response(e)