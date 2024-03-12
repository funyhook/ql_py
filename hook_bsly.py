# """
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 2024-01-12 14:30:38
# 微信小程序：#小程序://百事乐元/KEuBH5phXkXUaSA
# 反馈群：https://t.me/vhook_wool
# 抓包域名：https://pepcoinbhhpre.pepcoinbypepsico.com.cn 任意请求中的请求头【token】
# export hook_bsly=token@token
# cron：0 0 7 * * ?
#
# """
"""
new Env('百事乐园');
0 7 * * * hook_bsly.py
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
        self.token = ck['token']+","+ck['openid']
        self.name = None
        self.id = None
        self.index = i + 1
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        self.headers = {
            'Content-Type': 'application/json',
            "User-Agent": self.ua,
            "token": self.token,
            "Host": "pepcoinbhhpre.pepcoinbypepsico.com.cn"
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getUserInfo(self):
        # 获取openid
        url = "https://pepcoinnew.pepcoinbypepsico.com.cn/api/v1/wxapp/doGetUserInfo"
        data = {
            "token": self.token.split(",")[0],
            "provision": "2_0_6"

        }
        headers = {
            'Content-Type': 'application/json',
            "User-Agent": self.ua,
            "Host": "pepcoinnew.pepcoinbypepsico.com.cn"
        }
        response = self.ss.post(url=url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                self.name = res["data"]["mobile"]
                self.id = res["data"]["l_id"]
                return True
            else:
                return False
        return False

    def draw(self):
        url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/draw"
        response = self.ss.get(url=url, headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                return res['data']['name']
        return ""

    def getDrawCount(self):
        url = "https://pepcoinbhhpre.pepcoinbypepsico.com.cn/mp/getDrawCount"
        response = self.ss.get(url=url, headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0:
                return res['data']
        return 0

    def run(self):
        print(f"*********开始第{self.index}用户*********")
        msg = f"\n*********开始第{self.index}用户*********"
        if self.getUserInfo():
            print(f"[{self.index}]用户{self.name} ID:{self.id}")
            msg += f"\n[{self.index}]用户{self.name} ID:{self.id}"
            count = self.getDrawCount()
            print(f"[{self.index}]剩余抽奖次数：{count}")
            msg += f"\n[{self.index}]剩余抽奖次数：{count}"
            if count > 0:
                for no in range(count):
                    time.sleep(random.randint(3, 5))
                    res = self.draw()
                    print(f"[{self.index}]第{no + 1}次抽奖结果：{res}")
                    msg += f"\n[{self.index}]第{no + 1}次抽奖结果：{res}"
            else:
                print(f'[{self.index}]今日抽奖次数已用完，明天再来！')
                msg += f'\n[{self.index}]今日抽奖次数已用完，明天再来！'
        return msg


def get_env(key):
    if os.environ.get(key) is None:
        print(f"未填写环境变量{key}")
        return os.environ.get(key)
    else:
        return os.environ.get(key)


if __name__ == '__main__':
    print("【版本】：20240312001")
    print("【更新内容】：优化")
    print("【TG群】：https://t.me/vhook_wool")
    env_str = get_env("hook_bsly")
    if not env_str:
        print("未填写环境变量:export hook_bsly=token@token")
        exit()
    envs = json.loads(env_str)
    print(f"本次共发现{len(envs)}个ck")
    push_msg = ""
    for i, env in enumerate(envs):
        task = TASK(i, env)
        push_msg += task.run()
        time.sleep(random.randint(3, 5))
    notify.send("百事乐元推送", push_msg)
