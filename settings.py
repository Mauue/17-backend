DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = '17'

try:
    from local import *
except ModuleNotFoundError:
    pass