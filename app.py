from flask import Flask
from json import dumps
from controllers import init_app
from config import config
from db import DB


def create_app():
    app = Flask(__name__)

    init_app(app)

    app.config.from_mapping(config)

    DB.create_db(app)

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
