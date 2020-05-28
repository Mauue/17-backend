type_list = []
# type_list = {
#     "project_create": "创建了项目 {project}。",
#     "project_join": "加入了项目 {project}。",
#
#     "task_create": "创建了任务",
#     "task_finish": "完成了任务",
#     "task_redo": "重做了任务",
#     "task_update_name": "更新了任务 {task} 名字为 {name}。",
#     "task_update_remarks": "更新了任务 {task} 备注为 {remarks}。"
# }


class _Type:
    def __init__(self, name, content):
        self._content = content
        self._name = name
        type_list.append(self)

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content


project_create = _Type("project_create", "创建了项目")
project_join = _Type("project_join", "加入了项目")
project_leave = _Type("project_leave", "离开了项目")
project_add_admin = _Type("project_add_admin", "成为了管理员")
project_remove_admin = _Type("project_remove_admin", "不再是管理员")
project_delete = _Type("project_delete", "删除了项目")

task_create = _Type("task_create", "创建了任务")
task_finish = _Type("task_finish", "完成了任务")
task_redo = _Type("task_redo", "重做了任务")
task_update = _Type("task_update", "更新了任务")
task_delete = _Type("task_delete", "删除了任务")
task_add_participant = _Type("task_add_participant", "添加了参与者")
task_remove_participant = _Type("task_remove_participant", "移除了参与者")

schedule_create = _Type("schedule_create", "创建了日程")
schedule_update = _Type("schedule_update", "更新了日程")
schedule_delete = _Type("schedule_delete", "删除了日程")

