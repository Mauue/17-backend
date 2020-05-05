from lib.code import code_list
from model.schedule import Schedule
from model.user import User
from model.project import Project
from .project import before_project_service


def before_schedule_service(pid, user, sid) -> (code_list.CodeWithMessage, Project, Schedule):
    e, p = before_project_service(pid=pid, user=user)
    if e is not None:
        return e, None, None

    s = Schedule.get_by_id(sid)
    if s is None or not p.has_schedule(s):
        return code_list.ScheduleNoExists, None, None

    return None, p, s


def schedule_list(pid, user):
    e, p = before_project_service(pid, user)
    if e is not None:
        return e, None

    return code_list.Success, p.get_schedule_list()


def schedule_create(pid, user, content, remarks, t_set, t_remind, label):
    e, p = before_project_service(pid, user)
    if e is not None:
        return e, None

    if len(label) > 5:
        if not all([len(la) <= 5 for la in label.split(' ')]):
            return code_list.LabelTooLong

    s = Schedule.new(content, p.id, user.id, remarks=remarks, t_set=t_set, t_remind=t_remind,
                     label=label)
    return code_list.Success


def schedule_update(sid, pid, user, content, remarks, t_set, label):
    e, p, s = before_schedule_service(pid=pid, user=user, sid=sid)
    if e is not None:
        return e

    if len(label) > 5:
        if not all([len(la) <= 5 for la in label.split(' ')]):
            return code_list.LabelTooLong

    s.update(content=content, remarks=remarks, t_set=t_set, label=label)
    return code_list.Success


def schedule_delete(sid, pid, user):
    e, p, s = before_schedule_service(pid=pid, user=user, sid=sid)
    if e is not None:
        return e

    s.delete()
    return code_list.Success

