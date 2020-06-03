from lib.code import code_list
from model.group import Group
from model.project import Project
from model.user import User
from model.action import Action
from lib.action_list import action_type


def before_project_service(pid, user, is_admin=False) -> (code_list.CodeWithMessage, Project):
    p = Project.get_project_by_id(pid)
    if p is None:
        return code_list.ProjectNoExists, None
    if not p.has_member(user):
        return code_list.NotPermission, None
    if is_admin and not p.has_member(user, is_admin=is_admin):
        return code_list.NotProjectAdmin, None
    return None, p


def new_project(name, user):
    p = Project.new(name, user)

    Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_create.name,
               content=name, link=p.link)

    return code_list.Success, {
        "id": p.id
    }


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

    g = Group.query.filter_by(project_id=project_id, is_all=True).first()

    if is_add:
        if p.has_member(user):
            return code_list.InProject

        p.add_member(user)
        g.add(user)
        Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_join.name,
                   content=p.name, link=p.link)
    else:
        if not p.has_member(user):
            return code_list.NotInProject
        p.remove_member(user)
        g.remove(user)
        Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_leave.name,
                   content=p.name, link=p.link)
    return code_list.Success


def project_delete(project_id, user):
    c, p = before_project_service(project_id, user)
    if c is not None:
        return c
    if p.user_id != user.id:
        return code_list.NotProjectOriginator
    p.delete()
    Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_delete.name,
               content=p.name, link=p.link)
    return code_list.Success


def project_manage_admin(project_id, user_id, admin, is_add=True):
    c, p = before_project_service(project_id, admin)
    if c is not None:
        return c
    if p.user_id != admin.id:
        return code_list.NotProjectOriginator

    user = User.get_user_by_id(user_id)
    if user is None:
        return code_list.UserNotExist

    if user.id == admin.id:
        return code_list.OperatorError
    if not p.has_member(user):
        return code_list.NotInProject

    if is_add:
        p.add_admin(user)
        Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_add_admin.name,
                   content=p.name, link=p.link)
    else:
        p.remove_admin(user)
        Action.new(user_id=user.id, project_id=p.id, type_name=action_type.project_remove_admin.name,
                   content=p.name, link=p.link)
    return code_list.Success

