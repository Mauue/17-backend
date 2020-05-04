from lib.code import code_list
from .base import *
from .user import login_required, login_user_required
from flask import Blueprint, g
from model.project_form import *
from model.project import Project
from services import project as service

project_bp = Blueprint('project', __name__, url_prefix='/api')


@project_bp.route('/project', methods=["POST"])
@login_user_required
def new_project_controller():
    form = ProjectCreateForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong)
    id = int(g.user.id)
    pid = service.new_project(form.name.data, id)
    return response(code_list.Success, {"id": pid})


@project_bp.route('/project/<_project_id>')
@login_user_required
def project_info(_project_id):
    try:
        pid = int(_project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)
    user = g.user
    c, d = service.project_info(pid, user)
    return response(c, d)


@project_bp.route('/project/<_project_id>/user/add', methods=['POST'])
@login_user_required
def project_add_user(_project_id):
    try:
        pid = int(_project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    form = ProjectMemberManageForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user
    c = service.project_member_manage(project_id=pid, account=form.account.data,
                                      admin=user, account_type=form.account_type.data)
    return response(c)


@project_bp.route('/project/<_project_id>/user/remove', methods=['POST'])
@login_user_required
def project_remove_user(_project_id):
    try:
        pid = int(_project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    form = ProjectMemberManageForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong)

    user = g.user

    c = service.project_member_manage(pid, form.id.data, user, is_add=False)
    return response(c)


@project_bp.route('/user/project')
@login_user_required
def project_list():
    user = g.user
    return response(code_list.Success, user.project_list())