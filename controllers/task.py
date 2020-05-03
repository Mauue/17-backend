from lib.code import code_list
from model.task_form import TaskCreateForm
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g, request
from model.project_form import *
from model.project import Project
from services import task as service


task_bp = Blueprint('task', __name__, url_prefix='/api')


@task_bp.route('/project/<project_id>/task', methods=['POST', 'GET'])
@login_user_required
def task_list(project_id):
    try:
        pid = int(project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    user = g.user

    if request.method == "GET":
        e, d = service.task_list(pid, user)
        return response(e, d)
    else:
        form = TaskCreateForm()
        if not form.validate():
            return response(code_list.ParamsWrong.with_message(form.errors))

        e = service.task_create(pid, user, name=form.name.data, remarks=form.remarks.data,
                                t_begin=form.t_begin.data, t_end=form.t_end.data,
                                priority=form.priority.data, label=form.label.data)
        return response(e)


