from flask import Blueprint,request
from .base import response
from lib.code import code_list
from db import DB

bp = Blueprint('api', __name__, url_prefix='/api/test')


@bp.route('/v1')
def test_v1():
    return response(code_list.Success)


@bp.route('/v2')
def test_v2():
    name = request.args.get('name')

    if not name:
        return response(code_list.WrongParams)
    return response(code_list.Success, {name: name})


@bp.route('/v3')
def test_v3():
    print(DB.instance().test())
    return response(code_list.Success)