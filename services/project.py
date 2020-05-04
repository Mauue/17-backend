from lib.code import code_list
from model.project import Project
from model.user import User


def new_project(name, user_id):
    p = Project(name, user_id)
    id = p.create_new_project()
    return id


def project_info(project_id, user):
    p = Project.get_project_by_id(project_id)
    if p is None:
        return code_list.ProjectNoExists, None
    if not p.is_project_member(user):
        return code_list.NotPermission, None
    return code_list.Success, {
        "name": p.name,
        "member": p.get_project_member_list()
    }


def project_member_manage(project_id, member_id, admin, is_add=True):
    p = Project.get_project_by_id(project_id)
    if p is None:
        return code_list.ProjectNoExists
    if not p.is_project_member(admin, is_admin=True):
        return code_list.NotProjectAdmin

    user = User.get_user_by_id(member_id)
    if user is None:
        return code_list.UserNotExist

    if user.id == admin.id:
        return code_list.OperatorError

    if is_add:
        if p.is_project_member(user):
            return code_list.InProject

        p.add_member(user)
    else:
        if not p.is_project_member(user):
            return code_list.NotInProject
        p.remove_member(user)
    return code_list.Success

