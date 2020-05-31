import functools

from flask import Blueprint, request, session, g
from .base import *
from lib.code import code_list
from model.user_form import *
from services import chat as service
from .user import login_user_required
import re
chat_bp = Blueprint('chat', __name__, url_prefix='/api')


@chat_bp.route("/project/<_project_id>/chat/sig")
@login_user_required
def chat_get_sig(_project_id):
    e, pid = parse_project_id(_project_id)
    if e:
        return response(e)

    user = g.user
    e, d = service.get_sig(user=user, project_id=pid)
    return response(e, data=d)


@chat_bp.route("/project/<_project_id>/chat/group")
@login_user_required
def get_user_group(_project_id):
    e, pid = parse_project_id(_project_id)
    if e:
        return response(e)

    user = g.user
    e, d = service.get_groups(project_id=pid, user=user)
    return response(e, d)