from flask_wtf.csrf import CSRFError
from .base import response, csrf
from lib.code import code_list


def csrf_init_app(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        print("error", e)
        return response(code_list.CSRFError.with_message(str(e)))

    csrf.init_app(app)