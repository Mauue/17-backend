import threading
import oss2
import settings
import uuid
from http import HTTPStatus


class _OSS(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.auth = oss2.Auth(settings.AccessKeyId, settings.AccessKeySecret)
        self.bucket = oss2.Bucket(self.auth, settings.BucketRegion, settings.BucketName)

        try:
            self.bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            raise Exception("error")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with _OSS._instance_lock:
                if not hasattr(cls, '_instance'):
                    _OSS._instance = super().__new__(cls)

        return _OSS._instance

    def upload_photo(self, file, file_extension, old_file):
        filename = ''.join(str(uuid.uuid4()).split('-')) + '.' + file_extension
        result = self.bucket.put_object(settings.BucketPhotoPath+filename, file)
        success = result.status == HTTPStatus.OK
        if success and old_file:
            self.bucket.delete_object(old_file.split('.com/')[-1])
        return success, settings.BucketHost + settings.BucketPhotoPath + filename


oss = _OSS()

