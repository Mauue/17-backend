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
