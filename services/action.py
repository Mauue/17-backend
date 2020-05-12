from lib.code import code_list
from .project import before_project_service
from model.action import Action


def get_action_list_by_project(user, pid):
    e, p = before_project_service(pid, user)
    if e is not None:
        return e, None
    l = Action.get_list_by_project(p.id)
    return code_list.Success, l

