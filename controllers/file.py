from lib.code import code_list
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from services import file as service

file_bp = Blueprint('file', __name__, url_prefix='/api')


@file_bp.route('/project/<project_id>/file')
@login_user_required
def task_list(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    prefix = request.args.get('path') or ''
    user = g.user
    e, d = service.get_file_list(project_id=pid, user=user, prefix=prefix)
    return response(e, d)

