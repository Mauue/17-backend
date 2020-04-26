from lib import code
from flask import jsonify


def response(c: code.CodeWithMessage, data=None):
    return jsonify({
        'status': c.code,
        'msg': c.msg,
        'data': data
    })