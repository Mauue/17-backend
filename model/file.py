from . import db
from .oss import oss


class File:

    @staticmethod
    def get_file_list(project_id, prefix):
        prefix = str(project_id) + '/' + prefix
        if not prefix.endswith('/'):
            prefix += '/'
        return oss.get_file_list(prefix)

