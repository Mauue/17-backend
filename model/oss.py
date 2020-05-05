import threading
import oss2
import settings
import uuid
from http import HTTPStatus


class _OSS(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.auth = oss2.Auth(settings.AccessKeyId, settings.AccessKeySecret)
        self.public_bucket = oss2.Bucket(self.auth, settings.PublicBucketRegion,
                                         settings.PublicBucketName)
        self.private_bucket = oss2.Bucket(self.auth, settings.PrivateBucketRegion,
                                          settings.PrivateBucketName)

        try:
            self.public_bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            raise Exception("error")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with _OSS._instance_lock:
                if not hasattr(cls, '_instance'):
                    _OSS._instance = super().__new__(cls)

        return _OSS._instance

    def upload_photo(self, file, file_extension, old_file) -> (bool, str):
        filename = ''.join(str(uuid.uuid4()).split('-')) + '.' + file_extension
        result = self.public_bucket.put_object(settings.PublicBucketPhotoPath + filename, file)
        success = result.status == HTTPStatus.OK
        if success and old_file:
            self.public_bucket.delete_object(old_file.split('.com/')[-1])
        return success, settings.PublicBucketHost + settings.PublicBucketPhotoPath + filename

    def get_file_list(self, prefix):
        file_dict = {
            "directory": [],
            "file": []
        }
        for f in oss2.ObjectIterator(bucket=self.private_bucket, prefix=prefix, delimiter='/'):
            if f.key == prefix:
                continue
            if f.is_prefix():
                file_dict["directory"].append({
                    "name": str(f.key).lstrip(prefix)
                })
            else:
                file_dict["file"].append({
                    "filename": str(f.key).lstrip(prefix),
                    "size": f.size
                })
        return file_dict


oss = _OSS()

