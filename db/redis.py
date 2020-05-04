from flask_redis import FlaskRedis
import threading


class Redis(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self._client = FlaskRedis()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Redis._instance_lock:
                if not hasattr(cls, '_instance'):
                    Redis._instance = super().__new__(cls)

        return Redis._instance

    def init_app(self, app):
        self._client.init_app(app)

    def set(self, name, value, expire=None):
        self._client.set(name, value)
        if expire is not None:
            self._client.expire(name, expire)

    def get(self, name):
        result = self._client.get(name)
        return str(result, encoding="utf8") if result else result

