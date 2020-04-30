from flask import Blueprint
from .test import bp as test_bp
from .user import user_bp
from .csrf import csrf_init_app

blueprint_list = [test_bp, user_bp]


def init_app(app):
    for bp in blueprint_list:
        app.register_blueprint(bp)
    csrf_init_app(app)
