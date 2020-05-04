import os

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'b17'
base_dir = os.path.abspath(os.curdir)

AccessKeyId = ""
AccessKeySecret = ""
BucketName = ""
BucketRegion = ""
BucketHost = ""

try:
    from local import *
except ModuleNotFoundError:
    pass