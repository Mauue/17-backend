from lib import code
from flask import jsonify
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()


def response(c: code.CodeWithMessage, data=None):
    resp = jsonify({
        'status': c.code,
        'msg': c.msg,
        'data': data
    })
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

