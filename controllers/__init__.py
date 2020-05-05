from flask import Blueprint

from .file import file_bp
from .schedule import schedule_bp
from .task import task_bp
from .test import bp as test_bp
from .user import user_bp
from .csrf import csrf_init_app
from .project import project_bp
from flask.json import JSONEncoder
from datetime import datetime

blueprint_list = [test_bp, user_bp, project_bp, task_bp, schedule_bp, file_bp]


class _CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat(sep=' ')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def init_app(app):
    for bp in blueprint_list:
        app.register_blueprint(bp)
    csrf_init_app(app)
    app.json_encoder = _CustomJSONEncoder
