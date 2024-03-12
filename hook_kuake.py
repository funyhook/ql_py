"""
* 代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
* new Env("夸克签到")
* cron: 12 0 * * *
* 反馈群：https://t.me/vhook_wool
抓包教程：浏览器打开 https://pan.quark.cn ，复制全部cookie
export hook_kuaike="[
    {
        'name':'ls',
        'cookie': 'cookie'
    }
]"
"""
import json
import logging
import os
import time
import requests
from datetime import datetime

from utils import common
import notify

logging.basicConfig(level=logging.INFO)


class KUAKE:
    def __init__(self, no, account):
        self.msg = ''
        self.index = no
        self.name = account['name']
        self.cookie = account['cookie']

    def get_growth_info(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        headers = {
            "cookie": self.cookie,
            "content-type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, params=querystring).json()

        if response.get("data"):
            data = response.get("data")
            if data['cap_sign']['sign_daily']:
                msg = f"【签到】：今日已签到+{int(data['cap_sign']['sign_daily_reward'] / 1024 / 1024)}MB，📅 连签进度({data['cap_sign']['sign_progress']}/{data['cap_sign']['sign_target']})✅"
                self.msg += f"\n{msg}"
                self.log(msg)
            else:
                sign, sign_return = self.get_growth_sign()
                if sign:
                    msg = f"【签到】：执行签到: 今日签到+{int(sign_return / 1024 / 1024)}MB，📅 连签进度({data['cap_sign']['sign_progress'] + 1}/{data['cap_sign']['sign_target']})✅"
                    self.msg += f"\n{msg}"
                    self.log(msg)
                else:
                    msg = f"【签到】：执行签到: {sign_return}"
                    self.msg += f"\n{msg}"
                    self.log(msg)
            return response["data"]
        else:
            return False

    def get_info(self):
        url = "https://pan.quark.cn/account/info?fr=pc&platform=pc"
        querystring = {"fr": "pc", "platform": "pc"}
        headers = {
            "cookie": self.cookie,
            "content-type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        msg = f"【昵称】：{response['data']['nickname']}"
        self.msg += msg
        self.log(msg)

    def get_member_info(self):
        url = "https://drive-pc.quark.cn/1/clouddrive/member?pr=ucpro&fr=pc&uc_param_str=&fetch_subscribe=true&_ch=home&fetch_identity=true"
        headers = {
            "cookie": self.cookie,
            "content-type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, ).json()
        if response['data']:
            data = response['data']
            msg = f"【空间】：{int(data['use_capacity'] / 1024 / 1024)}MB/{int(data['total_capacity'] / 1024 / 1024 / 1024)}GB"
            self.msg += f"\n{msg}"
            self.log(msg)

    def get_growth_sign(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        payload = {
            "sign_cyclic": True,
        }
        headers = {
            "cookie": self.cookie,
            "content-type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers, params=querystring).json()
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def log(self, msg):
        print(f"用户{self.index}【{self.name}】：{msg}")

    def run(self):
        self.log(f"{'=' * 13}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}开始运行{'=' * 13}")
        self.get_info()
        self.get_member_info()
        self.get_growth_info()
        return self.msg


def getEnv(key):  # line:343
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        exit(f'青龙变量【{key}】没有获取到!自动退出')
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        print(f"\n----------共获取到{len(env_str)}个账号----------\n")
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354


if __name__ == '__main__':
    common.check_cloud("hook_kuake", 1.1)
    time.sleep(1)
    accounts = getEnv("hook_kuake")
    push_msg = ''
    for index, ck in enumerate(accounts):
        abc = KUAKE(index + 1, ck)
        push_msg += abc.run()
    notify.send("夸克网盘", push_msg)
