# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2024-02-27 11:13:09
# 微信小程序：茶百道
# 反馈群：https://t.me/vhook_wool
# 默认抢轮询抢券10次
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 抓包域名：https://chabaidao-gateway2.shuxinyc.com任意请求中的请求头【CSESSION】
# export hook_cbd='[
#   {
#     "token":"xxxxx",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":"ls"
#   }
# ]'
"""
new Env('茶百道抢券');
59 59 13 * * * hook_cbd.py
"""
import json
import os
import random
import time
from datetime import datetime

import requests

import notify


class TASK:
    def __init__(self, index, ck):
        self.token = ck['token']
        self.name = ck['name']
        self.level = 0
        self.totalPoints = 0
        self.id = None
        self.mobile = None
        self.unionId = None
        self.wxmiOpenid = None
        self.cardId = None
        self.ids = []
        self.index = index + 1
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        if ck['ua']:
            self.ua = ck['ua']
        self.headers = {
            "CSESSION": self.token,
            'User-Agent': self.ua,
            'Content-Type': 'application/json',
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def hide_phone_number(self, phone_number):
        # 隐藏手机号中间四位数字
        hidden_number = phone_number[:3] + '****' + phone_number[-4:]
        return hidden_number

    def getUserGet(self):
        # 获取openid
        url = "https://chabaidao-gateway2.shuxinyc.com/hll-auth-client/user/get"
        data = {
            "token": self.token,
            "groupId": "317964",
            "memberSystemId": "21",
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "000":
                self.unionId = res['data']["wxmiOpenid"]
                self.wxmiOpenid = res['data']["wxmiOpenid"]
                return True
            else:
                return False
        return False

    def getUserInfo(self):
        url = "https://chabaidao-gateway2.shuxinyc.com/member2c/applet/selectMemberInfo"
        data = {
            "token": self.token,
            "groupId": "317964",
            "memberSystemId": "21",
            "appID": "wx2804355dbf8d15c3",
            "sourceType": 30
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "000":
                self.id = res["data"]["id"]
                self.name = res["data"]["name"]
                self.mobile = res["data"]["mobile"]
                return True
        return False

    def queryCalendarDetail(self):
        url = "https://chabaidao-gateway2.shuxinyc.com/calendar/mini/event/queryCalendarDetail"
        data = {
            "token": self.token,
            "groupId": "317964",
            "memberSystemId": "21",
            "id": "22"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print("queryCalendarDetail:::" + response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 200:
                if len(res['data']['colCalendarConf']) > 0:
                    for col in res['data']['colCalendarConf']:
                        jumpUrl = col['eventCalendarCO']['jumpUrl']
                        self.ids.append(jumpUrl.split("eventID=")[1])

    def getCardDetail(self):
        url = "https://chabaidao-gateway2.shuxinyc.com/member2c/applet/card/queryCardForWechat"
        data = {
            "token": self.token,
            "groupId": "317964",
            "memberSystemId": "21",
            "appID": "wx2804355dbf8d15c3",
            "sourceType": 30,
            "mobile": self.mobile,
            "shopId": "-1",
            "openId": self.wxmiOpenid
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "000":
                self.cardId = res["data"][0]['id']

    def join(self, id):
        url = "https://chabaidao-gateway2.shuxinyc.com/marketing/minip/activity/joinActivity"
        data = {
            "token": self.token,
            "groupId": "317964",
            "memberSystemId": "21",
            "id": id,
            "activetype": 23,
            "unionId": self.unionId,
            "shopId": -1,
            "cardId": str(self.cardId),
            "mobile": self.mobile,
            "memberName": self.name
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "000":
                return True, res['msg']
            else:
                return False, res['msg']
        return False, "异常，请重试"

    def run(self):
        info = f"*********开始第{self.index}用户*********"
        print(info)
        msg = f"\n{info}"
        info = f"【用户{self.index}】备注：{self.name}"
        print(info)
        msg += f"\n{info}"
        if self.getUserInfo():
            info = f"【用户{self.index}】用户ID：{self.id}"
            info += f"\n【用户{self.index}】手机号：{self.hide_phone_number(self.mobile)}"
            print(info)
            msg += f"\n{info}"
            self.queryCalendarDetail()
            self.getCardDetail()

            for no in range(10):
                for aid in self.ids:
                    flag, rst = self.join(aid)
                    if flag:
                        info = f"【用户{self.index}】抢券结果：成功！"
                    else:
                        info = f"【用户{self.index}】抢券结果：{rst}"
                    print(info)
                    msg += f"\n{info}"

        else:
            info = f"【用户{self.index}】token 失效"
            print(info)
            msg += f"\n{info}"
        return msg


def get_env(key: str) -> str:
    if os.environ.get(key) is None:
        print(f"未填写环境变量{key}")
        return os.environ.get(key)
    else:
        return os.environ.get(key)


if __name__ == '__main__':
    env_str = get_env("hook_cbd")
    # env_str = '[{"token":"1709019526|1LcPxFSNaEbMNK0L.i1StrV1w0z+mOtfzBMU5QhWX0Rr7m4aXYlKZGNXoEEumYDF5mB5+mu295rTCr6YrWTuOnZSZbInE3UYsGbLmGQ==.967f25638dcb9cff","ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181","name":"ls"}]'
    if not env_str:
        exit()
    envs = json.loads(env_str)
    print(f"本次共发现{len(envs)}个ck")
    push_msg = ""
    for i, env in enumerate(envs):
        task = TASK(i, env)
        push_msg += task.run()
        time.sleep(random.randint(3, 5))
    notify.send("茶百道抢券推送", push_msg)
