from . import db
from .oss import oss
from .user import User


class File:

    @staticmethod
    def get_file_list(project_id, prefix):
        prefix = str(project_id) + '/' + prefix.lstrip('/')
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
        print(path)
        return oss.upload_file(path=path, file=file, tag=tag)

