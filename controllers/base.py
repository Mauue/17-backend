from lib import code
from flask import jsonify
from flask_wtf.csrf import CSRFProtect

from lib.code import code_list

csrf = CSRFProtect()


def response(c: code.CodeWithMessage, data=None):
    resp = jsonify({
        'status': c.code,
        'msg': c.msg,
        'data': data
    })
    return resp


def parse_project_id(_pid):
    try:
        pid = int(_pid)
    except ValueError:
        return code_list.ProjectNoExists, None
    return None, pid