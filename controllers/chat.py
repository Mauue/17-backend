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
    try:
        pid = int(_project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    user = g.user
    e, d = service.get_sig(user=user, project_id=pid)
    return response(e, data=d)

