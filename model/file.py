from . import db
from .oss import oss
from .user import User


class File:

    @staticmethod
    def get_file_list(project_id, prefix):
        prefix = str(project_id) + '/' + prefix.strip('/')
        if not prefix.endswith('/'):
            prefix += '/'
        l = oss.get_file_list(prefix)
        for file in l["file"]:
            id = int(file['upload'])
            user = User.get_user_by_id(int(id))
            file['upload'] = {
                "id": user.id,
                "username": user.username,
                "photo": user.photo
            }
        return l

    @staticmethod
    def upload_file(project_id, path, file, filename, tag):
        path = path.strip('/') + '/' + filename
        path = str(project_id) + '/' + path.strip('/')
        return oss.upload_file(path=path, file=file, tag=tag)

    @staticmethod
    def download_file(project_id, path):
        path = str(project_id) + '/' + path.strip('/')
        if not oss.exist_file(path):
            return None
        return oss.download_file(path)

    @staticmethod
    def delete_file(project_id, path):
        path = str(project_id) + '/' + path.lstrip('/')
        if not oss.exist_file(path):
            return None
        return oss.delete_file(path)

    @staticmethod
    def delete_files(project_id, paths):
        new_paths = []
        for path in paths:
            path = str(project_id) + '/' + path.lstrip('/')
            new_paths.append(path)
        r = oss.delete_files(new_paths)
        return True

