from lib.code import code_list
from model.task_form import *
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
    except ValueError:
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


@task_bp.route('/project/<project_id>/task/info')
@login_user_required
def task_info(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    task_id = request.args.get("id")
    user = g.user
    e, d = service.get_task_info_by_id(user=user, project_id=pid, task_id=task_id)
    return response(e, d)


@task_bp.route('/project/<project_id>/task/update', methods=['POST'])
@login_user_required
def task_update(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    form = TaskUpdateForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user
    e = service.task_update(task_id=form.id.data, user=user, name=form.name.data,
                            remarks=form.remarks.data, label=form.label.data, priority=form.priority.data,
                            t_begin=form.t_begin.data, t_end=form.t_end.data, project_id=pid,
                            finish=form.finish.data)
    return response(e)


@task_bp.route('/project/<project_id>/task/delete', methods=['POST'])
@login_user_required
def task_delete(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    form = TaskDeleteForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user
    e = service.task_delete(task_id=form.id.data, user=user, project_id=pid)
    return response(e)


@task_bp.route('/project/<project_id>/task/participant/add', methods=['POST'])
@login_user_required
def task_add_participant(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    form = TaskManageParticipant()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user

    e = service.task_manage_participant(task_id=form.task_id.data, project_id=pid,
                                        participant_id=form.user_id.data, user=user, is_add=True)
    return response(e)


@task_bp.route('/project/<project_id>/task/participant/remove', methods=['POST'])
@login_user_required
def task_remove_participant(project_id):
    try:
        pid = int(project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    form = TaskManageParticipant()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user

    e = service.task_manage_participant(task_id=form.task_id.data, project_id=pid,
                                        participant_id=form.user_id.data, user=user, is_add=False)
    return response(e)

