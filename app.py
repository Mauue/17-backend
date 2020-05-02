from flask import Flask
from json import dumps
from controllers import init_app
from config import config
from db import db_init_app


def create_app():
    app = Flask(__name__)

    init_app(app)

    app.config.from_mapping(config)

    db_init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
