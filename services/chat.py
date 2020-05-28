from model.im import IM
from lib.code import code_list


def get_sig(user):
    success = IM.create_account(user_id=user.id)
    if success:
        return code_list.Success, IM.gen_user_sig(user_id=user.id)
    return code_list.OtherError, None

