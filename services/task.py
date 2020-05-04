from lib.code import code_list
from model.task import Task
from model.user import User
from model.project import Project


def task_list(pid, user):
    project = Project.get_project_by_id(pid)
    if project is None:
        return code_list.ProjectNoExists, None

    if not project.is_project_member(user):
        return code_list.NotPermission, None

    return code_list.Success, project.get_task_list()


def task_create(project_id, user, name, remarks, t_begin, t_end, priority, label):
    p = Project.get_project_by_id(project_id)
    if p is None:
        return code_list.ProjectNoExists
    if not p.is_project_member(user):
        return code_list.NotPermission

    if len(label) > 5:
        if not all([len(la) <= 5 for la in label.split(' ')]):
            return code_list.LabelTooLong

    Task.new_task(name, p.id, user.id, remarks=remarks, t_begin=t_begin, t_end=t_end,
                  priority=priority, label=label)
    return code_list.Success


def task_update(task_id, user, project_id, name, remarks, t_begin, t_end, priority, label, finish):
    task = Task.get_task_by_id(task_id)
    if task is None:
        return code_list.TaskNoExists

    project = Project.get_project_by_id(project_id)
    if project is None:
        return code_list.ProjectNoExists
    if not project.is_project_member(user):
        return code_list.NotPermission

    if not project.has_task(task):
        return code_list.TaskNoExists

    task.update(name=name, remarks=remarks, t_begin=t_begin,
                t_end=t_end, priority=priority, label=label, finish=finish)
    return code_list.Success


def task_delete(task_id, user, project_id):
    task = Task.get_task_by_id(task_id)
    if task is None:
        return code_list.TaskNoExists

    project = Project.get_project_by_id(project_id)
    if project is None:
        return code_list.ProjectNoExists
    if not project.is_project_member(user):
        return code_list.NotPermission

    if not project.has_task(task):
        return code_list.TaskNoExists

    task.delete()
    return code_list.Success