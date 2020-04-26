from . import config
from settings import *

config.update(
    {
        "DB_URL": 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

    }
)