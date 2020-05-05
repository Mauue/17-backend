from lib.code import code_list
from .project import before_project_service
from model.file import File


def get_file_list(project_id, user, prefix):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c, None
    f = File.get_file_list(project_id=project_id, prefix=prefix)
    return code_list.Success, f
