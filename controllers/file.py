from lib.code import code_list
from model.file_form import *
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from services import file as service

file_bp = Blueprint('file', __name__, url_prefix='/api')


@file_bp.route('/project/<project_id>/file', methods=["POST", "GET"])
@login_user_required
def file_info(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    if request.method == "GET":
        prefix = request.args.get('path') or ''
        user = g.user
        e, d = service.get_file_list(project_id=pid, user=user, prefix=prefix)
        return response(e, d)
    else:
        form = FileUploadForm()
        if not form.validate():
            return response(code_list.ParamsWrong.with_message(form.errors))

        user = g.user

        e = service.upload_file(pid, file=form.file.data, path=form.path.data, user=user)
        return response(e)


@file_bp.route('/project/<project_id>/file/download')
@login_user_required
def file_get_url(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    path = request.args.get("path")
    if not path:
        return response(code_list.ParamsWrong)
    user = g.user

    e, url = service.download_file(project_id=pid, path=path, user=user)
    return response(e, url)


@file_bp.route('/project/<project_id>/file/delete', methods=["POST"])
@login_user_required
def file_delete(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    form = FileDeleteForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user

    e = service.delete_file(pid, user=user, path=form.path.data)
    return response(e)


@file_bp.route('/project/<project_id>/file/delete_batch', methods=["POST"])
@login_user_required
def file_delete_batch(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    form = FilesDeleteForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user

    e = service.delete_files(pid, user=user, paths=form.paths.data.split(' '))
    return response(e)

