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
    user = g.user
    e, d = service.new_project(form.name.data, user)
    return response(e, d)


@project_bp.route('/project/<_project_id>')
@login_user_required
def project_info(_project_id):
    try:
        pid = int(_project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    user = g.user
    c, d = service.project_info(pid, user)
    return response(c, d)


@project_bp.route('/project/<_project_id>/delete', methods=['POST'])
@login_user_required
def project_delete(_project_id):
    try:
        pid = int(_project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)
    user = g.user
    c = service.project_delete(pid, user)
    return response(c)


@project_bp.route('/project/<_project_id>/user/add', methods=['POST'])
@login_user_required
def project_add_user(_project_id):
    try:
        pid = int(_project_id)
    except ValueError:
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
    except ValueError:
        return response(code_list.ProjectNoExists)

    form = ProjectMemberManageForm()
    if not form.validate():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user

    c = service.project_member_manage(project_id=pid, account=form.account.data,
                                      admin=user, account_type=form.account_type.data, is_add=False)
    return response(c)


@project_bp.route('/user/project')
@login_user_required
def project_list():
    user = g.user
    return response(code_list.Success, user.project_list())


@project_bp.route('/project/<_project_id>/admin/add', methods=['POST'])
@login_user_required
def project_add_admin(_project_id):
    try:
        pid = int(_project_id)
    except TypeError:
        return response(code_list.ProjectNoExists)

    form = ProjectAdminManageForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user
    c = service.project_manage_admin(project_id=pid, user_id=form.id.data, admin=user)
    return response(c)


@project_bp.route('/project/<_project_id>/admin/remove', methods=['POST'])
@login_user_required
def project_remove_admin(_project_id):
    try:
        pid = int(_project_id)
    except ValueError:
        return response(code_list.ProjectNoExists)

    form = ProjectAdminManageForm()
    if not form.validate_on_submit():
        return response(code_list.ParamsWrong.with_message(form.errors))

    user = g.user
    c = service.project_manage_admin(project_id=pid, user_id=form.id.data, admin=user, is_add=False)
    return response(c)

