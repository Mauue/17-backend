from flask import Blueprint

from .action import action_bp
from .chat import chat_bp
from .file import file_bp
from .remind import remind_bp
from .schedule import schedule_bp
from .task import task_bp
from .test import bp as test_bp
from .user import user_bp
from .csrf import csrf_init_app
from .project import project_bp
from flask.json import JSONEncoder
from datetime import datetime
from flask_wtf.csrf import CSRFError

blueprint_list = {test_bp, user_bp, project_bp, task_bp, schedule_bp, file_bp, action_bp,
                  chat_bp, remind_bp}


class _CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat(sep=' ')
            elif isinstance(obj, CSRFError):
                print(obj)
                return obj
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
