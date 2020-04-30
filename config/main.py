from . import config
from settings import *

config.update(
    {
        "SQLALCHEMY_DATABASE_URI": 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    }
)