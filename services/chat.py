from config import config
from model.group import Group
from model.im import IM
from lib.code import code_list
from services.project import before_project_service


def get_sig(project_id, user):
    e, p = before_project_service(pid=project_id, user=user)
    if e is not None:
        return e, None

    success = IM.create_account(user=user, project_id=project_id)
    IM.update_account(project_id=project_id, user_id=user.id, username=user.username, photo=user.photo)
    data = {
        "app_id": config["IM_APP_ID"],
        "user_id": IM.gen_user_identify(user_id=user.id, project_id=project_id),
        "user_sig": IM.gen_user_sig(user_id=user.id, project_id=project_id)
    }

    if success:
        return code_list.Success, data
    return code_list.OtherError, None


def get_groups(project_id, user):
    e, p = before_project_service(pid=project_id, user=user)
    if e is not None:
        return e, None
    groups = Group.get_by_project_id(project_id)
    data = [
        {
            "im_id": g.im_id,
            "name": g.name,
            "is_all": g.is_all
        } for g in groups
    ]
    return code_list.Success, data

