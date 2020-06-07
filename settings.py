import os

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'b17'
base_dir = os.path.abspath(os.curdir)

AccessKeyId = ""
AccessKeySecret = ""
PublicBucketName = ""
PublicBucketRegion = ""
PublicBucketHost = ""

PublicBucketPhotoPath = "img/photo/"

PrivateBucketName = ""
PrivateBucketRegion = ""
PrivateBucketOutRegion = ""
PrivateBucketHost = ""

IMAppID = ""
IMAppSecret = ""
IMAdmin = ""

try:
    from local import *
except ModuleNotFoundError:
    pass

