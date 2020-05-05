from lib.code import code_list
from model.file_form import FileUploadForm
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from services import file as service

file_bp = Blueprint('file', __name__, url_prefix='/api')


@file_bp.route('/project/<project_id>/file', methods=["POST", "GET"])
@login_user_required
def task_list(project_id):
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
