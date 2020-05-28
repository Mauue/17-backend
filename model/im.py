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

    @classmethod
    def gen_user_sig(cls, user_id):
        return cls.tls_api.gen_sig(user_id)

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
    def create_account(cls, user_id, username=None, user_photo=None):
        api = "im_open_login_svc/account_import"
        data = {"Identifier": str(user_id)}
        if username is not None:
            data["Nick"] = username
        if user_photo is not None:
            data["FaceUrl"] = user_photo

        resp = cls._send_rest(api, data)
        if resp and resp["ErrorCode"] == 0:
            return True
        if resp is not None:
            logging.warning("create_account Error:" + str(resp))
        return False

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

