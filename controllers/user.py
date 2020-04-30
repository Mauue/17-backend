from flask import Blueprint, request, session
from .base import *
from lib.code import code_list
from model.user_form import *

user_bp = Blueprint('user', __name__, url_prefix='/api')


@user_bp.route('/user/register', methods=['POST', 'GET'])
@csrf.exempt
def register_user():
    form = UserRegisterForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))
    return response(code_list.Success, {
        "type": form.account_type.data,
        "password": form.password.data
    })


@user_bp.route('/user/login', methods=['POST'])
def login_user():
    form = UserLoginForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))
    session['account'] = form.account.data
    return response(code_list.Success, {
        "type": form.account_type.data,
        "password": form.password.data
    })


@user_bp.route('/user/logout')
def logout_user():
    session.clear()
    return response(code_list.Success)


@user_bp.route('/user/info')
def info_user():
    account = session.get('account')
    return response(code_list.Success, {
        "name": account
    })


