from . import CodeWithMessage

# 全局
Success = CodeWithMessage(0, '操作成功')
OtherError = CodeWithMessage(-1, '系统错误')
ParamsWrong = CodeWithMessage(-100, '参数错误')
CSRFError = CodeWithMessage(-101, '认证失败')


# 用户模块
PhoneFormatWrong = CodeWithMessage(1001, '手机号格式错误')
EmailFormatWrong = CodeWithMessage(1002, '邮箱格式错误')
PasswordFormatWrong = CodeWithMessage(1003, '密码格式错误')
PhoneNoExists = CodeWithMessage(1004, '手机号不存在')
EmailNoExists = CodeWithMessage(1005, '邮箱不存在')
PasswordWrong = CodeWithMessage(1006, '密码错误')

