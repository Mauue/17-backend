from flask_wtf.csrf import CSRFError
from .base import response, csrf
from lib.code import code_list


def csrf_init_app(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        print("error")
        return response(code_list.CSRFError.with_message(e))

    csrf.init_app(app)