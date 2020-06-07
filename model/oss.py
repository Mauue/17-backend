import threading
import oss2
from oss2.headers import OSS_OBJECT_TAGGING
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
        self.private_out_bucket = oss2.Bucket(self.auth, settings.PrivateBucketOutRegion,
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
        l = len(prefix)
        file_dict = {
            "directory": [],
            "file": []
        }
        for f in oss2.ObjectIterator(bucket=self.private_bucket, prefix=prefix, delimiter='/'):
            if f.key.strip('/') == prefix.strip('/'):
                continue
            if f.is_prefix():
                file_dict["directory"].append({
                    "name": str(f.key)[l:]
                })
            else:
                tag = self.private_bucket.get_object_tagging(f.key)
                file_dict["file"].append({
                    "filename": str(f.key)[l:],
                    "upload": tag.tag_set.tagging_rule["upload"],
                    "size": f.size
                })
        return file_dict

    def upload_file(self, file, path, tag):
        headers = dict()
        headers[OSS_OBJECT_TAGGING] = tag
        if file is None:
            file = ""
            path = path.rstrip('/') + '/'
        result = self.private_bucket.put_object(path, file, headers=headers)
        success = result.status == HTTPStatus.OK
        return success

    def exist_file(self, path):
        print(path)
        return self.private_bucket.object_exists(path)

    def download_file(self, path):
        url = self.private_out_bucket.sign_url('GET', path, 60)
        return url

    def delete_file(self, path):
        print(path)
        if path.endswith('/'):
            self.delete_directory(path)
        return self.private_bucket.delete_object(path)

    def delete_files(self, paths):
        print(paths)
        for path in paths:
            if path.endswith('/'):
                self.delete_directory(path)
        return self.private_bucket.batch_delete_objects(paths)

    def delete_directory(self, path):
        if not path.endswith('/'):
            return
        for obj in oss2.ObjectIterator(self.private_bucket, prefix=path):
            self.private_bucket.delete_object(obj.key)


oss = _OSS()
