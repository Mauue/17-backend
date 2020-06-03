from lib.tls import TLSSigAPIv2
from config import config
from random import randrange
from json import dumps, loads
import logging
import requests


class IM:
    tls_api = TLSSigAPIv2(config["IM_APP_ID"], config["IM_APP_SECRET"])
    admin_user = config["IM_ADMIN"]
    admin_sig = tls_api.gen_sig(admin_user)

    @staticmethod
    def gen_user_identify(user_id, project_id):
        return "{pid}-{uid}".format(pid=project_id, uid=user_id)

    @classmethod
    def gen_user_sig(cls, user_id, project_id):
        return cls.tls_api.gen_sig(IM.gen_user_identify(user_id=user_id, project_id=project_id))

    @classmethod
    def _send_rest(cls, api, data):
        url = "https://console.tim.qq.com/v4/{api}?sdkappid={SDKAppID}&"\
            "identifier={identifier}&usersig={usersig}&random={random}&"\
            "contenttype=json".format(api=api, SDKAppID=config["IM_APP_ID"],
                                      identifier=cls.admin_user, usersig=cls.admin_sig,
                                      random=randrange(1, 99999999))
        r = requests.post(url, data=dumps(data))
        if r.status_code != 200:
            return None
        return loads(r.text)

    @classmethod
    def create_account(cls, project_id, user):
        api = "im_open_login_svc/account_import"
        data = {
            "Identifier": IM.gen_user_identify(user_id=user.id, project_id=project_id),
            "Nick": user.username,
            "FaceUrl": user.photo or ""
        }

        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return True
        if resp is not None:
            logging.warning("create_account Error:" + str(resp))
        return False

    @classmethod
    def update_account(cls, project_id, user_id, username, photo):
        api = "profile/portrait_set"
        data = {
            "From_Account": IM.gen_user_identify(user_id=user_id, project_id=project_id),
            "ProfileItem": [
                {
                    "Tag": "Tag_Profile_IM_Nick",
                    "Value": username,
                }, {
                    "Tag": "Tag_Profile_IM_Image",
                    "Value": photo or "",
                }
            ]

        }
        resp = cls._send_rest(api, data)
        print(resp, username, photo)
        if resp and resp["ErrorCode"] == 0:
            return True
        if resp is not None:
            logging.warning("create_account Error:" + str(resp))
        return False

    @classmethod
    def get_account_info(cls, project_id, user):
        api = "profile/portrait_get"
        data = {
            "Identifier": IM.gen_user_identify(user_id=user.id, project_id=project_id),
            "Nick": user.username,
            "FaceUrl": user.photo or ""
        }

        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return True
        if resp is not None:
            logging.warning("create_account Error:" + str(resp))
        return False

    @classmethod
    def delete_account_batch(cls, project_id, user_id_list):
        api = "im_open_login_svc/account_delete"
        data = {
            "DeleteItem": [
                {
                    "UserID": IM.gen_user_identify(user_id=user_id, project_id=project_id)
                } for user_id in user_id_list
            ]
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return True
        if resp is not None:
            logging.warning("create_account Error:" + str(resp))
        return False

    @classmethod
    def delete_account(cls, project_id, user_id):
        return cls.delete_account_batch(project_id, [user_id])

    @classmethod
    def check_account(cls, user_id):
        api = "im_open_login_svc/account_check"
        data = {
            "CheckItem": [
                {"UserID": user_id}
            ]
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return resp["ResultItem"]
        return None

    @classmethod
    def create_group(cls, user, name, pid, gid):
        if not IM.create_account(project_id=pid, user=user):
            return "cant create account"
        api = "group_open_http_svc/create_group"
        data = {
            "Owner_Account": IM.gen_user_identify(user_id=user.id, project_id=pid),
            "Type": "Private",
            "Name": name,
            "GroupId": "@b17#group"+str(gid)
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return None
        return resp

    @classmethod
    def destroy_group(cls, gid):
        api = "group_open_http_svc/destroy_group"
        data = {
            "GroupId": gid
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return None
        return resp

    @classmethod
    def joinGroup(cls, gid, user, pid):
        if not IM.create_account(project_id=pid, user=user):
            return "cant create account"
        api = "group_open_http_svc/add_group_member"
        print(gid)
        data = {
            "GroupId": str(gid),
            "Silence": 1,
            "MemberList": [
                {
                    "Member_Account": IM.gen_user_identify(user_id=user.id, project_id=pid),
                }
            ]
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return None
        return resp

    @classmethod
    def leaveGroup(cls, gid, uid, pid):
        api = "group_open_http_svc/delete_group_member"
        data = {
            "GroupId": str(gid),
            "Silence": 1,
            "MemberToDel_Account": [
                IM.gen_user_identify(user_id=uid, project_id=pid),
            ]
        }
        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return None
        return resp


if __name__ == "__main__":
    print(IM.check_account(IM.gen_user_identify(user_id=7, project_id=28)))
    pass