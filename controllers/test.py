from flask import Blueprint, request, render_template
from .base import response
from lib.code import code_list
from db import red, db
import os
import settings
from flask_wtf.csrf import generate_csrf
bp = Blueprint('api', __name__, url_prefix='/api/test')


@bp.route('/v1')
def test_v1():
    return response(code_list.Success)


@bp.route('/v2')
def test_v2():
    name = request.args.get('name')

    if not name:
        return response(code_list.ParamsWrong)
    return response(code_list.Success, {name: name})


@bp.route('/v3')
def test_v3():
    print(id(db))
    return response(code_list.Success)


@bp.route('/v4-1')
def test_red_1():
    red.set('test', '01', 10)
    return response(code_list.Success)


@bp.route('/v4-2')
def test_red_2():
    return response(code_list.Success, red.get('test'))


@bp.route('/fp')
def frontend_pull():
    msg = ""
    try:
        path = os.path.join(settings.base_dir, 'fp.sh')
        os.system(path)
    except Exception as e:
        msg = e
    return response(code_list.Success.with_message(msg))


@bp.route('/csrf')
def get_csrf():
    return response(code_list.Success, generate_csrf())