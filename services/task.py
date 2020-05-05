from lib.code import code_list
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

    Task.new(name, p.id, user.id, remarks=remarks, t_begin=t_begin, t_end=t_end,
             priority=priority, label=label)
    return code_list.Success


def task_update(task_id, user, project_id, name, remarks, t_begin, t_end, priority, label, finish):
    c, project, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    task.update(name=name, remarks=remarks, t_begin=t_begin,
                t_end=t_end, priority=priority, label=label, finish=finish)
    return code_list.Success


def task_delete(task_id, user, project_id):
    c, project, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    task.delete()
    return code_list.Success


def task_manage_participant(task_id, user, project_id, participant_id, is_add=True):
    c, project, task = before_task_service(pid=project_id, tid=task_id, user=user)
    if c is not None:
        return c

    user = User.get_user_by_id(participant_id)
    if user is None:
        return code_list.UserNotExist
    if not project.has_member(user):
        return code_list.NotInProject

    if is_add:
        if task.has_participant(user):
            return code_list.InParticipant
        task.add_participant(user)
    else:
        if not task.has_participant(user):
            return code_list.NotInParticipant
        task.remove_participant(user)
    return code_list.Success

