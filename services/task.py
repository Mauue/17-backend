from lib.code import code_list
from lib.action_list import action_type
from model.action import Action
from model.task import Task
from model.user import User
from model.project import Project
from .project import before_project_service


def before_task_service(pid, user, tid) -> (code_list.CodeWithMessage, Project, User):
    c, project = before_project_service(pid, user)
    if c is not None:
        return c, None, None

    task = Task.get_task_by_id(tid)
    if task is None:
        return code_list.TaskNoExists, None, None
    if not project.has_task(task):
        return code_list.TaskNoExists, None, None
    return None, project, task


def task_list(pid, user):
    project = Project.get_project_by_id(pid)
    if project is None:
        return code_list.ProjectNoExists, None

    if not project.has_member(user):
        return code_list.NotPermission, None

    return code_list.Success, project.get_task_list()


def task_create(project_id, user, name, remarks, t_begin, t_end, priority, label):
    c, p = before_project_service(pid=project_id, user=user)
    if c is not None:
        return c
    if len(label) > 5:
        if not all([len(la) <= 5 for la in label.split(' ')]):
            return code_list.LabelTooLong

    task = Task.new(name, p.id, user.id, remarks=remarks, t_begin=t_begin, t_end=t_end,
                    priority=priority, label=label)
    Action.new(user_id=user.id, project_id=p.id, type_name=action_type.task_create.name,
               content=name, link=task.link)
    return code_list.Success


def task_update(task_id, user, project_id, name, remarks, t_begin, t_end, priority, label, finish):
    c, p, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    task.update(name=name, remarks=remarks, t_begin=t_begin,
                t_end=t_end, priority=priority, label=label, finish=finish)
    Action.new(user_id=user.id, project_id=p.id, type_name=action_type.task_update.name,
               content=name, link=task.link)
    return code_list.Success


def task_delete(task_id, user, project_id):
    c, p, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    task.delete()
    Action.new(user_id=user.id, project_id=p.id, type_name=action_type.task_delete.name,
               content=task.name, link=task.link)
    return code_list.Success


def task_manage_participant(task_id, user, project_id, participant_id, is_add=True):
    c, p, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    participant = User.get_user_by_id(participant_id)
    if participant is None:
        return code_list.UserNotExist
    if not p.has_member(participant):
        return code_list.NotInProject

    if is_add:
        if task.has_participant(participant):
            return code_list.InParticipant
        task.add_participant(participant)
        Action.new(user_id=user.id, project_id=p.id,
                   type_name=action_type.task_add_participant.name,
                   content=participant.username, link=task.link)
    else:
        if not task.has_participant(participant):
            return code_list.NotInParticipant
        task.remove_participant(participant)
        Action.new(user_id=user.id, project_id=p.id,
                   type_name=action_type.task_remove_participant.name,
                   content=participant.username, link=task.link)
    return code_list.Success


def get_task_info_by_id(user, project_id, task_id):
    e, p, t = before_task_service(pid=project_id, user=user, tid=task_id)
    if e is not None:
        return e, None, None
    task_info = {
        "id": t.id,
        "name": t.name,
        "remarks": t.remarks,
        "finish": t.finish,
        "originator": {
            "id": t.user_id,
            "username": t.originator.username,
            "photo": t.originator.photo
        },
        "t_begin": t.t_begin,
        "t_end": t.t_end,
        "priority": t.priority,
        "label": t.label,
        "participants": [{
            "id": p.id,
            "username": p.username,
            "photo": p.photo
        } for p in t.participants]
    }
    return code_list.Success, task_info
