from lib.code import code_list
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from services import action as service

action_bp = Blueprint('action', __name__, url_prefix='/api')


@action_bp.route('/project/<project_id>/action')
@login_user_required
def project_action_list(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    user = g.user

    e, d = service.get_action_list_by_project(user=user, pid=pid)
    return response(e, d)


