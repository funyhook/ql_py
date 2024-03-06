# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2024-02-27 11:13:09
# 微信小程序：奈雪的茶
# 反馈群：https://t.me/vhook_wool

# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 抓包域名：https://tm-api.pin-dao.cn任意请求中的请求头【Authorization】
# export hook_nxdc='[
#   {
#     "token":"Bearer 123456",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":"ls"
#   }
# ]'
"""
new Env('奈雪的茶');
0 7 * * * hook_nxdc.py
"""
import base64
import hmac
import json
import math
import os
import random
import time
from datetime import datetime
from hashlib import sha1

import requests

import notify


class TASK:
    def __init__(self, i, ck):
        self.token = ck['token']
        self.name = ck['name']
        self.level = 0
        self.totalPoints = 0
        self.id = None
        self.index = i + 1
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        if ck['ua']:
            self.ua = ck['ua']
        self.headers = {
            'User-Agent': self.ua,
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'Host': 'tm-api.pin-dao.cn',
            'Connection': 'keep-alive',
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.ex_timeMills = math.floor(time.time())
        self.nonce = math.floor(1e6 * random.random())
        self.openId = "QL6ZOftGzbziPlZwfiXM"
        self.a = "nonce=" + str(self.nonce) + "&openId=" + self.openId + "&timestamp=" + str(self.ex_timeMills);
        self.signStr = self.signure()

    def hide_phone_number(self, phone_number):
        # 隐藏手机号中间四位数字
        hidden_number = phone_number[:3] + '****' + phone_number[-4:]
        return hidden_number

    def hash_hmac(self, key, code):
        hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
        return base64.b64encode(hmac_code).decode()

    def signure(self):
        return self.hash_hmac("sArMTldQ9tqU19XIRDMWz7BO5WaeBnrezA", self.a)

    def getUserInfo(self):
        # 获取openid
        url = "https://tm-api.pin-dao.cn/user/base-userinfo"
        data = {
            "common": {
                "platform": "wxapp",
                "version": "5.2.8",
                "imei": "",
                "osn": "MacBookPro18,3",
                "sv": "Mac OS X 14.3.1",
                "lang": "zh_CN",
                "currency": "CNY",
                "timeZone": "",
                "nonce": self.nonce,
                "openId": self.openId,
                "timestamp": self.ex_timeMills,
                "signature": self.signStr
            },
            "params": {
                "businessType": 1,
                "brand": 26000252,
                "tenantId": 1,
                "channel": 2,
                "stallType": None,
                "storeId": "",
                "storeType": "",
                "cityId": "",
                "appId": "wxab7430e6e8b9a4ab"
            }
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.userId = res['data']["userId"]
                self.phone = res['data']["phone"]
                self.nickName = res['data']["nickName"]
                self.joiningDate = res['data']["joiningDate"]
                return True
            else:
                return False
        return False

    def getUserAccount(self):
        url = "https://tm-web.pin-dao.cn/user/account/user-account"
        data = {
            "common": {
                "platform": "wxapp",
                "version": "5.2.8",
                "imei": "",
                "osn": "MacBookPro18,3",
                "sv": "Mac OS X 14.3.1",
                "lat": 39.976265233265515,
                "lng": 116.48424382823944,
                "lang": "zh_CN",
                "currency": "CNY",
                "timeZone": "",
                "nonce": self.nonce,
                "openId": self.openId,
                "timestamp": self.ex_timeMills,
                "signature": self.signStr
            },
            "params": {
                "businessType": 1,
                "brand": 26000252,
                "tenantId": 1,
                "channel": 2,
                "stallType": "PD_S_004",
                "storeId": 26073975,
                "storeType": 1,
                "cityId": 110100,
                "appId": "wxab7430e6e8b9a4ab"
            }
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.coin = res["data"]["coin"]
                self.remainMoney = res["data"]["remainMoney"]

    def getSignRecords(self):
        url = "https://tm-web.pin-dao.cn/user/sign/records"
        data = {
            "common": {
                "platform": "wxapp",
                "version": "5.2.8",
                "imei": "",
                "osn": "MacBookPro18,3",
                "sv": "Mac OS X 14.3.1",
                "lat": 39.976265233265515,
                "lng": 116.48424382823944,
                "lang": "zh_CN",
                "currency": "CNY",
                "timeZone": "",
                "nonce": self.nonce,
                "openId": self.openId,
                "timestamp": self.ex_timeMills,
                "signature": self.signStr
            },
            "params": {
                "businessType": 1,
                "brand": 26000252,
                "tenantId": 1,
                "channel": 2,
                "stallType": "PD_S_004",
                "storeId": 26073975,
                "storeType": 1,
                "cityId": 110100,
                "appId": "wxab7430e6e8b9a4ab",
                "signDate": "2024-2-01",
                "startDate": "2024-2-27"
            }
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['success']:
                self.signDays = res['data']['signCount']
                return res['data']['status']

    def doSign(self):
        url = "https://tm-web.pin-dao.cn/user/sign/save"
        data = {
            "common": {
                "platform": "wxapp",
                "version": "5.2.8",
                "imei": "",
                "osn": "MacBookPro18,3",
                "sv": "Mac OS X 14.3.1",
                "lat": 39.976265233265515,
                "lng": 116.48424382823944,
                "lang": "zh_CN",
                "currency": "CNY",
                "timeZone": "",
                "nonce": self.nonce,
                "openId": self.openId,
                "timestamp": self.ex_timeMills,
                "signature": self.signStr
            },
            "params": {
                "businessType": 1,
                "brand": 26000252,
                "tenantId": 1,
                "channel": 2,
                "stallType": "PD_S_004",
                "storeId": 26073975,
                "storeType": 1,
                "cityId": 110100,
                "appId": "wxab7430e6e8b9a4ab",
                "signDate": self.dateStr
            }
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['success']:
                self.sing_res = res['data']['infos']
                return res['data']['flag']
        return False

    def run(self):
        info = f"*********开始第{self.index}用户*********"
        print(info)
        msg = f"\n{info}"
        info = f"【用户{self.index}】备注：{self.name}"
        print(info)
        msg += f"\n{info}"
        if self.getUserInfo():

            info = f"【用户{self.index}】用户ID：{self.userId}"
            info += f"\n【用户{self.index}】注册日期：{self.joiningDate}"
            info += f"\n【用户{self.index}】手机号：{self.hide_phone_number(self.phone)}"
            print(info)
            msg += f"\n{info}"
            self.getUserAccount()
            info = f"【用户{self.index}】奈雪币：{self.coin}"
            print(info)
            msg += f"\n{info}"
            status = self.getSignRecords()
            if status:
                info = f"【用户{self.index}】签到结果：今日已签到"
                print(info)
                msg += f"\n{info}"
            else:
                if self.doSign():
                    info = f"【用户{self.index}】签到结果：成功"
                    print(info)
                    msg += f"\n{info}"
                    self.getSignRecords()
                else:
                    info = f"【用户{self.index}】签到结果：失败"
                    print(info)
                    msg += f"\n{info}"
            info = f"【用户{self.index}】签到天数：{self.signDays}"
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
    env_str = get_env("hook_nxdc")
    # env_str = '[{"token":"Bearer ","ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181","name":"ls"}]'
    if not env_str:
        exit()
    envs = json.loads(env_str)
    print(f"本次共发现{len(envs)}个ck")
    push_msg = ""
    for i, env in enumerate(envs):
        task = TASK(i, env)
        push_msg += task.run()
        time.sleep(random.randint(3, 5))
    notify.send("奈雪的茶推送", push_msg)
