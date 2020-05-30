from lib.code import code_list
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from services import remind as service

remind_bp = Blueprint('remind', __name__, url_prefix='/api')


@remind_bp.route('/project/<project_id>/remind')
@login_user_required
def project_remind_list(project_id):
    e, pid = parse_project_id(project_id)
    if e:
        return response(e)

    user = g.user

    e, d = service.get_remind(user=user, project_id=pid)
    return response(e, d)


