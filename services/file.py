from lib.code import code_list
from .project import before_project_service
from model.file import File


def get_file_list(project_id, user, prefix):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c, None
    f = File.get_file_list(project_id=project_id, prefix=prefix)
    return code_list.Success, f


def upload_file(project_id, user, file, path):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c
    filename = file.filename if file else ''
    path = path or ""

    s = File.upload_file(project_id=project_id, file=file, path=path, filename=filename,
                         tag="upload=%s" % user.id)
    if s:
        return code_list.Success
    return code_list.OtherError


def download_file(project_id, user, path):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c, None
    url = File.download_file(project_id, path)
    if url:
        return code_list.Success, url
    return code_list.FileNoExists, None


def delete_file(project_id, user, path):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c, None
    r = File.delete_file(project_id, path)
    if r is None:
        return code_list.FileNoExists
    return code_list.Success


def delete_files(project_id, user, paths):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c, None
    File.delete_files(project_id, paths)

    return code_list.Success
