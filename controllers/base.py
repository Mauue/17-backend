from lib import code
from flask import jsonify
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def response(c: code.CodeWithMessage, data=None):
    return jsonify({
        'status': c.code,
        'msg': c.msg,
        'data': data
    })

