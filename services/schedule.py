from lib.code import code_list
from model.schedule import Schedule
from model.user import User
from model.project import Project


def schedule_list(pid, user):
    project = Project.get_project_by_id(pid)
    if project is None:
        return code_list.ProjectNoExists, None

    if not project.is_project_member(user):
        return code_list.NotPermission, None

    return code_list.Success, project.get_schedule_list()


def schedule_create(project_id, user, content, remarks, t_set, t_remind, label):
    p = Project.get_project_by_id(project_id)
    if p is None:
        return code_list.ProjectNoExists
    if not p.is_project_member(user):
        return code_list.NotPermission

    if len(label) > 5:
        if not all([len(la) <= 5 for la in label.split(' ')]):
            return code_list.LabelTooLong

    s = Schedule(content, p.id, user.id, remarks=remarks, t_set=t_set, t_remind=t_remind,
                 label=label)
    s.new()
    return code_list.Success
