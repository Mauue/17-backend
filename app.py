from flask import Flask
from json import dumps
import controllers
from db import DB


def create_app():
    app = Flask(__name__)

    DB.create_db(app)

    for bp in controllers.blueprint_list:
        app.register_blueprint(bp)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/test')
    def test():
        return dumps({
            'status': 0,
            'msg': 'ok',
            'data': None
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
