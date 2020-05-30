from lib.code import code_list
from .project import before_project_service
from model.action import Action


def get_remind(user, project_id):
    e, p = before_project_service(user=user, pid=project_id)
    if e is not None:
        return e, None
    return code_list.Success, p.get_remind_by_user(user)

