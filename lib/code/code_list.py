from . import CodeWithMessage

# 全局
Success = CodeWithMessage(0, '操作成功')
OtherError = CodeWithMessage(-1, '系统错误')
ParamsWrong = CodeWithMessage(-100, '参数错误')
CSRFError = CodeWithMessage(-101, '认证失败')
NoLogin = CodeWithMessage(-102, '未登录')
OperatorError = CodeWithMessage(-103, '错误操作')
FileSizeTooBig = CodeWithMessage(-104, '文件过大')


# 用户模块
PhoneFormatWrong = CodeWithMessage(1002, '手机号格式错误')
EmailFormatWrong = CodeWithMessage(1001, '邮箱格式错误')
PasswordFormatWrong = CodeWithMessage(1003, '密码格式错误')
PhoneNoExists = CodeWithMessage(1004, '手机号不存在')
EmailNoExists = CodeWithMessage(1005, '邮箱不存在')
PasswordWrong = CodeWithMessage(1006, '密码错误')
EmailExists = CodeWithMessage(1007, '邮箱已存在')
PhoneExists = CodeWithMessage(1008, '手机号已存在')
UsernameFormatWrong = CodeWithMessage(1009, '用户名含非法字符')
UserNotExist = CodeWithMessage(1010, '用户不存在')


# 项目模块
ProjectNoExists = CodeWithMessage(2001, '项目不存在')
NotPermission = CodeWithMessage(2002, '无权访问该项目')
NotProjectAdmin = CodeWithMessage(2003, '非项目管理员')
NotProjectOriginator = CodeWithMessage(2004, '非项目创建者')
InProject = CodeWithMessage(2005, '成员已经加入项目')
NotInProject = CodeWithMessage(2006, '成员未加入项目')


# 任务模块
TaskNoExists = CodeWithMessage(3001, '任务不存在')
InParticipant = CodeWithMessage(3002, '成员已经参与任务')
NotInParticipant = CodeWithMessage(3003, '成员未参与任务')


# 文件模块
FileNoExists = CodeWithMessage(4001, '文件不存在')


# 日程模块
ScheduleNoExists = CodeWithMessage(5001, '日程不存在')


# 群聊模块

# 其他模块
LabelTooLong = CodeWithMessage(9001, '标签过长')

