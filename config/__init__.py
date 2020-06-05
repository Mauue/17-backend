from settings import *

config = {
    "SQLALCHEMY_DATABASE_URI": "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECRET_KEY": b'IV\xb0\x91]\xd0\xa3V%\x1c\xa0\xe99kt\x1a',
    "SESSION_COOKIE_HTTPONLY": False,
    "WTF_CSRF_ENABLED": False,
    "REDIS_URL": "redis://:@localhost:6379/0",
    "IM_APP_ID": IMAppID,
    "IM_APP_SECRET": IMAppSecret,
    "IM_ADMIN": IMAdmin
}


