from lib.code import code_list
from model.schedule_form import ScheduleCreateForm
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from model.project_form import *
from model.project import Project
from services import schedule as service


schedule_bp = Blueprint('schedule', __name__, url_prefix='/api')


@schedule_bp.route('/project/<project_id>/schedule', methods=['POST', 'GET'])
@login_user_required
def schedule_list(project_id):
    try:
        pid = int(project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    user = g.user

    if request.method == "GET":
        e, d = service.schedule_list(pid, user)
        return response(e, d)
    else:
        form = ScheduleCreateForm()
        if not form.validate():
            return response(code_list.ParamsWrong.with_message(form.errors))

        e = service.schedule_create(pid, user, content=form.content.data, remarks=form.remarks.data,
                                    t_set=form.t_set.data, t_remind=form.t_remind.data,
                                    label=form.label.data)
        return response(e)

