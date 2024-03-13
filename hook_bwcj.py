# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2024-02-27 11:13:09
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 微信小程序：霸王茶姬
#反馈群：https://t.me/vhook_wool
# 抓包域名：https://webapi.qmai.cn任意请求中的请求头【qm-user-token】
# export hook_bwcj='[
#   {
#     "token":"KsZCd6TDWtHDuG6wHun_acSIfuo3eAd6Nu9LPPpu_C6k26Xp7nA1t_NJy1MdI7ys",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":"ls"
#   }
# ]'
"""
new Env('霸王茶姬');
0 7 * * * hook_bwcj.py
"""
import json
import os
import random
import time
from datetime import datetime

import requests

from utils import notify


class TASK:
    def __init__(self, i, ck):
        self.token = ck['token']
        self.name = ck['name']
        self.level = 0
        self.totalPoints = 0
        self.id = None
        self.index = i + 1
        if ck['ua']:
            self.ua = ck['ua']
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        self.headers = {
            'qm-user-token': self.token,
            'User-Agent': self.ua,
            'qm-from': 'wechat',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': 'webapi.qmai.cn',
            'Connection': 'keep-alive',
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getUserInfo(self):
        # 获取openid
        url = "https://webapi.qmai.cn/web/catering/crm/customer-center?appid=wxafec6f8422cb357b"
        response = self.ss.get(url=url, headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.level = res['data']["customerCenterCardLevelInfo"]["level"]
                return True
            else:
                return False
        return False

    def getUserPoint(self):
        # 获取openid
        url = "https://webapi.qmai.cn/web/catering/crm/points-info"
        data = {
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.totalPoints = res["data"]["totalPoints"]

    def getSignInfo(self):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/userSignStatistics"
        data = {
            "activityId": "947079313798000641",
            "bizScene": 1,
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        # print(response.text)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.signDays = res['data']['signDays']
                self.signStatus = res['data']['signStatus']

    def doSign(self):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign"
        data = {
            "activityId": "947079313798000641",
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['status'] :
                return True
        return False

    def run(self):
        print(f"*********开始第{self.index}用户*********")
        print(f"【用户{self.index}】备注：{self.name}")
        msg = f"\n*********开始第{self.index}用户*********"
        msg += f"\n【用户{self.index}】备注：{self.name}"
        if self.getUserInfo():
            print(f"【用户{self.index}】等级：Level {self.level}")
            msg += f"\n【用户{self.index}】等级：Level {self.level}"
            self.getUserPoint()
            print(f"【用户{self.index}】积分：{self.totalPoints}")
            msg += f"\n【用户{self.index}】积分：{self.totalPoints}"
            self.getSignInfo()
            print(f"【用户{self.index}】已签到：{self.signDays} 天")
            msg += f"\n【用户{self.index}】已签到：{self.signDays} 天"
            if self.signStatus == 2:
                if self.doSign():
                    print(f"【用户{self.index}】签到：签到成功！")
                    msg += f"\n【用户{self.index}】签到：签到成功"
                else:
                    print(f"【用户{self.index}】签到：签到失败！")
                    msg += f"\n【用户{self.index}】签到：签到失败"
            else:
                print(f"【用户{self.index}】签到：今日已签到！")
        else:
            print(f"【用户{self.index}】token 失效")
            msg += f"\n【用户{self.index}】token 失效"
        return msg


def get_env(key):
    if os.environ.get(key) is None:
        print(f"未填写环境变量{key}，自动退出！")
        exit()
    else:
        return os.environ.get(key)


if __name__ == '__main__':
    print("【版本】：20240312001")
    print("【更新内容】：优化")
    print("【TG群】：https://t.me/vhook_wool")
    env_str = get_env("hook_bwcj")
    # env_str = '[{"token":"KsZCd6TDWtHDuG6wHun_acSIfuo3eAd6Nu9LPPpu_C6k26Xp7nA1t_NJy1MdI7ys","ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181","name":"ls"}]'

    envs = json.loads(env_str)
    print(f"本次共发现{len(envs)}个ck")
    push_msg = ""
    for i, env in enumerate(envs):
        task = TASK(i, env)
        push_msg += task.run()
        time.sleep(random.randint(3, 5))
    notify.send("霸王茶姬推送", push_msg)
