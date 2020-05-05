from lib.code import code_list
from model.project import Project
from model.user import User


def before_project_service(pid, user) -> (code_list.CodeWithMessage, Project):
    p = Project.get_project_by_id(pid)
    if p is None:
        return code_list.ProjectNoExists, None
    if not p.has_member(user):
        return code_list.NotPermission, None
    return None, p


def new_project(name, user_id):
    p = Project(name, user_id)
    id = p.create_new_project()
    return id


def project_info(project_id, user):
    c, p = before_project_service(pid=project_id, user=user)
    if c is not None:
        return c, None

    return code_list.Success, {
        "name": p.name,
        "member": p.get_project_member_list()
    }


def project_member_manage(project_id, account, admin, is_add=True, account_type="id"):
    c, p = before_project_service(pid=project_id, user=admin)
    if c is not None:
        return c

    if account_type == "email":
        user = User.get_user_by_email(account)
    elif account_type == "phone":
        user = User.get_user_by_phone(account)
    elif account_type == "id":
        user = User.get_user_by_id(account)
    else:
        return code_list.ParamsWrong.with_message("未开放类型")

    if user is None:
        return code_list.UserNotExist

    if user.id == admin.id:
        return code_list.OperatorError

    if is_add:
        if p.has_member(user):
            return code_list.InProject

        p.add_member(user)
    else:
        if not p.has_member(user):
            return code_list.NotInProject
        p.remove_member(user)
    return code_list.Success
