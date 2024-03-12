"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
# 反馈群：https://t.me/vhook_wool
new Env("ikuuu签到")
cron: 12 0 * * *
反馈群：https://t.me/vhook_wool
注册入口：https://ikuuu.pw/auth/register?code=xLmV
export hook_ikuuu="[
    {
        'email': '邮箱',
        'pwd':'密码',
    }
]"
"""
import json
import logging
import os
import time
from datetime import datetime

import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

import requests

logging.basicConfig(level=logging.INFO)


class ikuuu():
    def __init__(self, no, account):
        self.msg = ''
        self.email = account['email']
        self.pwd = account['pwd']
        self.cks = ""
        self.index = no

    def sign(self):
        time.sleep(0.5)
        url = "https://ikuuu.pw/user/checkin"
        url1 = 'https://ikuuu.pw/user'
        login_url = 'https://ikuuu.pw/auth/login'

        login_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        data = {
            'email': self.email,
            'passwd': self.pwd
        }
        response = requests.post(login_url, headers=login_header, data=data)
        cookies = response.cookies
        cookies_dict = cookies.get_dict()
        for key, value in cookies_dict.items():
            ck = f"{key}={value}"
            self.cks += ck + ';'

        headers = {
            'Cookie': self.cks,
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        }
        time.sleep(0.5)
        r = requests.post(url, headers=headers)
        time.sleep(0.5)
        r1 = requests.get(url1, headers=headers)
        try:
            soup = BeautifulSoup(r1.text, 'html.parser')
            bs = soup.find('span', {'class': 'counter'})
            syll = bs.text
            dl = soup.find('div', {'class': 'd-sm-none d-lg-inline-block'})
            name = dl.text
        except:
            xx = f"[登录]：请检查ck有效性：{self.cks}\n\n"
            self.log(xx)
            self.msg += xx
            return self.msg

        if r.status_code != 200:
            xx = f"[签到]：请求失败，请检查网络或者ck有效性\n\n"
            self.log(xx)
            self.msg += xx
            return self.msg
        try:
            if "已经签到" in r.json()['msg']:
                xx = f"[签到]：{r.json()['msg']}\n[流量]：{syll}GB\n\n"
                self.log(f"[签到]：{r.json()['msg']}")
                self.log(f"[流量]：{syll}GB")
                self.msg += xx
                return self.msg
            elif "获得" in r.json()['msg']:
                xx = f"[签到]：{r.json()['msg']}\n[流量]：{syll}GB\n\n"
                self.log(f"[签到]：{r.json()['msg']}")
                self.log(f"[流量]：{syll}GB")
                self.msg += xx
                return self.msg
            else:
                xx = f"[签到]：未知错误，请检查网络或者ck有效性\n\n"
                self.log(xx)
                self.msg += xx
                return self.msg
        except:
            xx = f"[登录]：解析响应失败，请检查网络或者ck有效性：\n\n"
            self.log(xx)
            self.msg += xx
            return self.msg

    def log(self, msg):
        print(f"用户{self.index}【{self.email}】：{msg}")

    def run(self):
        self.log(f"{'=' * 13}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}开始运行{'=' * 13}")
        return self.sign()

def getEnv(key):  # line:343
    inviteUrl = 'https://ikuuu.pw/auth/register?code=xLmV'
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'青龙变量【{key}】没有获取到!自动退出；\n注册入口：{inviteUrl}')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        print(f"共获取到{len(env_str)}个账号")
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354
        print(f"活动入口：{inviteUrl}")


if __name__ == '__main__':
    print("ikuuu注册入口：https://ikuuu.pw/auth/register?code=xLmV")
    accounts = getEnv("hook_ikuuu")
    for index, ck in enumerate(accounts):
        abc = ikuuu(index + 1, ck)
        abc.run()
