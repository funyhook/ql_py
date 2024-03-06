# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2024-02-29 15:44:20
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 微信小程序：#小程序://家乐活动坊/L6vnHf9QcDNWzdK
# 反馈群：https://t.me/vhook_wool

# 抓包域名：https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/任意请求中参数中的【accessToken】
# export hook_jlhdf='[
#   {
#     "accessToken":"userId",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":"ls",
#   }
# ]'
"""
new Env('家乐活动坊');
0 7 * * * hook_jlhdf.py
"""
import json
import os
import random
import time
from datetime import datetime

import requests

import notify

js_str = """
function deal(res,tokenJs){
    window={}
    let code = /<script\\b[^>]*>\s*var([\s\S]*?)<\/script>/.exec(res)[1];
    eval(code)
    key = /var\s+key\s+=\s+'([^']+)';/.exec(getDuibaToken.toString())[1];
    s = eval(tokenJs);
    return window[key];
}
"""


class YongPai:
    def __init__(self, i, ck):
        self.token = ck['accessToken']
        self.name = ck['name']
        self.index = i + 1
        self.id = None
        if hasattr(ck, "ua") and ck['ua'] != "":
            self.ua = ck['ua']
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        self.headers = {
            'User-Agent': self.ua,
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.leaveTimes = 0
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.taskList = [
            {"task": "doReadAsk",
             "name": "问卷任务",
             "url": "https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/doReadAsk"
             },
            {"task": "doReadHot",
             "name": "大师招聘",
             "url": "https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/doReadHot"
             },
            {"task": "doReadAsk",
             "name": "家乐菜谱",
             "url": "https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/doReadCook"
             },
        ]

    def getUserInfo(self):
        url = f'https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/getUserInfo'
        data = {
            "accessToken": self.token,
            # "pid": None,
            "version": "202402"
        }
        headers = {
            'x-tingyun': 'c=M|PqG5aZfjT2U',
            "content-type": "application/json",
            "xweb_xhr": "1",
            'user-agent': self.ua,
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wx5bbb748be275b594/28/page-frame.html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        # print(f"{url}\n{data}\n{headers}\n{res.text}")
        if res.status_code == 200:
            rj = res.json()

            if rj['success'] == "1":
                self.leaveTimes = rj['userInfo']['leaveTimes']
        # print(f"getUserInfo===> {res.json()}")

    def dotask(self):
        url = f'https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/doReadAsk'
        data = {
            "accessToken": self.token,
        }
        headers = {
            'x-tingyun': 'c=M|PqG5aZfjT2U',
            "content-type": "application/json",
            "xweb_xhr": "1",
            'user-agent': self.ua,
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wx5bbb748be275b594/28/page-frame.html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        for task in self.taskList:
            res = requests.post(task['url'], data=json.dumps(data), headers=headers)
            # print(f"{url}\n{data}\n{headers}\n{res.text}")

            print(f"{task['name']}===> {res.json()}")

    def startPlay(self):
        url = f'https://crmwelfare2023.unileverfoodsolutions.com.cn/MobileApi/startPlay'
        current_time = datetime.now()
        current_milliseconds_timestamp = int(current_time.timestamp() * 1000)
        data = {
            "createTime": current_milliseconds_timestamp,
            "accessToken": "e1bc9da1-b6f8-4732-8739-2a40547c08c3"
        }
        print(data)
        headers = {
            'x-tingyun': 'c=M|PqG5aZfjT2U',
            "content-type": "application/json",
            "xweb_xhr": "1",
            'user-agent': self.ua,
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wx5bbb748be275b594/28/page-frame.html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            rj = res.json()
            if not hasattr(rj, "success"):
                print(res.text)
            else:
                if rj['success'] == "1":
                    print(f"抽奖结果：获得【{rj['rewardLog']['name']}】")
                else:
                    print(rj['message'])

    def run(self):
        print(f"{'-' * 20}第{self.index}个账号{'-' * 20}")
        print(f'用户【{self.name}】开始执行任务>>>')
        self.dotask()
        self.getUserInfo()
        print(f"抽奖次数：{self.leaveTimes}")
        if self.leaveTimes > 0:
            self.startPlay()


def getEnv(key):  # line:343
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'【{key}】青龙变量里没有获取到!自动退出')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        return env_str  # line:350
    except Exception as e:  # line:351
        print('错误:', e)  # line:352
        print('你填写的变量是:', env_str)  # line:353
        print('请检查变量参数是否填写正确')  # line:354


if __name__ == '__main__':
    accounts = getEnv("hook_yp")
    # accounts = [
    #     {
    #         "accessToken": "10265ac0-c82a-46d5-8aaf-accb712568c4",
    #         "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x1308070a) XWEB/1181",
    #         "name": "ls",
    #     }
    # ]
    print(f"本次共发现{len(accounts)}个ck")
    push_msg = ""
    for index, env in enumerate(accounts):
        YongPai(index, env).run()
        time.sleep(random.randint(3, 5))
    print("所有账号执行结束>>>")
    notify.send("甬派推送", push_msg)
