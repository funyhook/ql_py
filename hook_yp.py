# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2024-02-29 15:44:20
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# app：甬派
# 反馈群：https://t.me/vhook_wool

# 抓包域名：https://webapi.qmai.cn任意请求中的请求头【qm-user-token】
# export hook_yp='[
#   {
#     "userId":"userId",
#     "deviceId":"deviceId",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":"ls",
#     "zfbName":"支付宝姓名",
#     "zfbAccount":"支付宝账号"
#   }
# ]'
"""
new Env('甬派');
0 7 * * * hook_yp.py
"""
import json
import os
import random
import re
import time
import urllib
from datetime import datetime

import execjs
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
        self.key_str = None
        self.key = None
        self.autologin = None
        self.wdata = ""
        self.user_id = ck['userId']
        self.device_id = ck['deviceId']
        self.realName = ck['zfbName']
        self.account = ck['zfbAccount']
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
        self.window = {}
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_id(self):
        url = f'https://ypapp.cnnb.com.cn/yongpai-news/api/v2/news/list?channelId=0&currentPage=1&timestamp={int(time.time() * 1000)}'
        res = requests.get(url)
        for news in res.json()['data']['content']:
            if '转盘' in news.get('keywords', ''):
                news_id = news['channel'][0]['newsId']
                url = f'https://ypapp.cnnb.com.cn/yongpai-news/api/news/detail?newsId={news_id}&userId={self.user_id}'
                res = requests.get(url)
                self.id = re.search(r'\?id=(\d+)&?', res.json()['data']['body']).group(1)
                return

    def get_autologin(self):
        print()
        url = f'https://ypapp.cnnb.com.cn/yongpai-user/api/duiba/autologin?dbredirect=https%3A//92722.activity-12.m.duiba.com.cn/hdtool/index?id%3D{self.id}%26dbnewopen&userId={self.user_id}'
        self.autologin = requests.get(url).json()
        # print(f"get_autologin:: " + self.autologin['data'])

    def get_token(self):
        try:
            response = requests.get(self.autologin['data'], allow_redirects=False)
            wdata3_match = re.search(r'wdata3=(.*?)(?:;|$)', response.headers.get("Set-Cookie", ""))
            wdata4_match = re.search(r'wdata4=(.*?)(?:;|$)', response.headers.get("Set-Cookie", ""))
            # 检查是否成功匹配到"wdata3"和"wdata4"，并输出结果
            if wdata4_match:
                wdata4 = wdata4_match.group(1)
                self.wdata += f"wdata4={wdata4};"
            else:
                print("未找到wdata4")
            if wdata3_match:
                wdata3 = wdata3_match.group(1)
                self.wdata += f"wdata3={wdata3};"
            else:
                print("未找到wdata3")
        except Exception as e:
            print(e)
        url = f"https://92722.activity-12.m.duiba.com.cn/hdtool/index?id={self.id}&dbnewopen&from=login&spm=92722.1.1.1"
        headers = {
            'authority': '92722.activity-12.m.duiba.com.cn',
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self.wdata,
            'origin': 'https://92722.activity-12.m.duiba.com.cn',
            'pragma': 'no-cache',
            'referer': f"https://92722.activity-12.m.duiba.com.cn/hdtool/index?id={self.id}&dbnewopen&from=login&spm=92722.1.1.1",
            'user-agent': self.ua,
            'content-type': "application/x-www-form-urlencoded",
        }
        res = requests.get(url, headers=headers)
        url = 'https://92722.activity-12.m.duiba.com.cn/hdtool/ctoken/getTokenNew'
        data = f"timestamp={int(time.time() * 1000)}&activityId={self.id}&activityType=hdtool&consumerId=4066466507"
        ress = requests.post(url, data=data, headers=headers)
        tokenJs = ress.json()["token"]
        ctx = execjs.compile(js_str)
        self.key_str = ctx.call("deal", res.text, tokenJs)

    def do_task(self):
        url = f'https://ypapp.cnnb.com.cn/yongpai-news/api/v2/news/list?channelId=0&currentPage=1&timestamp={int(time.time() * 1000)}'
        res = requests.get(url, headers=self.headers)
        for item in res.json()['data']['content']:
            try:

                news_id = item['newsId']
                url = f'https://ypapp.cnnb.com.cn/yongpai-news/api/news/detail?newsId={news_id}&userId={self.user_id}'
                res = requests.get(url, headers=self.headers)
                print(f'阅读：[{item["title"]}]:✅\n' if res.json().get('message') == 'OK' else f'阅读：[{item["title"]}]:❌\n')
                time.sleep(random.randint(1, 2))

                like_headers = {"appversion": "10.1.4"}
                url = f'https://ypapp.cnnb.com.cn/yongpai-ugc/api/praise/save_news?deviceId={self.device_id}&newsId={news_id}&userId={self.user_id}'
                res = requests.get(url, headers=like_headers)
                print(f'点赞：[{item["title"]}]:✅\n' if res.json().get('message') == 'OK' else f'点赞：[{item["title"]}]:❌\n')
                time.sleep(random.randint(1, 2))

                url = f'https://ypapp.cnnb.com.cn/yongpai-ugc/api/forward/news?newsId={news_id}&source=4&userId={self.user_id}'
                res = requests.get(url, headers=self.headers)
                print(f'分享：[{item["title"]}]:✅\n' if res.json().get('message') == 'OK' else f'分享：[{item["title"]}]:❌\n')
                time.sleep(random.randint(1, 2))
            except Exception as e:  # line:351
                continue

    def do_join(self):
        url = f'https://92722.activity-12.m.duiba.com.cn/hdtool/doJoin?dpm=92722.3.1.0&activityId={self.id}&_={int(time.time() * 1000)}'
        data = f'actId={self.id}&oaId={self.id}&activityType=hdtool&consumerId=4066466507&token={self.key_str}'
        headers = {
            'authority': '92722.activity-12.m.duiba.com.cn',
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self.wdata,
            'origin': 'https://92722.activity-12.m.duiba.com.cn',
            'pragma': 'no-cache',
            'referer': f"https://92722.activity-12.m.duiba.com.cn/hdtool/index?id={self.id}&dbnewopen&from=login&spm=92722.1.1.1",
            'content-type': "application/x-www-form-urlencoded",
            'user-agent': self.ua,
        }
        res = requests.post(url, data=data, headers=headers)
        print(f"抽奖结果===> {res.json()}")

    def do_take_prize(self):
        url = f'https://92722.activity-12.m.duiba.com.cn/crecord/getrecord?page=1&_={int(time.time() * 1000)}'
        headers = {
            'authority': '92722.activity-12.m.duiba.com.cn',
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self.wdata,
            'origin': 'https://92722.activity-12.m.duiba.com.cn',
            'pragma': 'no-cache',
            'referer': f"https://92722.activity-12.m.duiba.com.cn/hdtool/index?id={self.id}&dbnewopen&from=login&spm=92722.1.1.1",
            # 'content-type': "application/x-www-form-urlencoded",
            'user-agent': self.ua,
        }
        res = requests.get(url, headers=headers)
        record_ids = []
        print("奖品记录：>>>>>")
        for record in res.json()['records']:

            recordId = json.loads(record['emdJson'])['info']
            if "待领" in record['statusText']:
                print(record)
                url = f'https://92722.activity-12.m.duiba.com.cn/activity/takePrizeNew?recordId={recordId}&dpm=92722.26.0.1&dcm=101.53.217692856808979.0&dbnewopen'
                res = requests.get(url, headers=headers)

                url = 'https://92722.activity-12.m.duiba.com.cn/ctoken/getToken.do'
                headers = {
                    'authority': '92722.activity-12.m.duiba.com.cn',
                    'accept': 'application/json',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': self.wdata,
                    'origin': 'https://92722.activity-12.m.duiba.com.cn',
                    'pragma': 'no-cache',
                    'referer': f"https://92722.activity-12.m.duiba.com.cn/hdtool/index?id={self.id}&dbnewopen&from=login&spm=92722.1.1.1",
                    'user-agent': self.ua,
                    'content-type': "application/x-www-form-urlencoded",
                }
                tokenJs = requests.post(url, headers=headers).json()['token']

                ctx = execjs.compile(js_str)
                self.key_str = ctx.call("deal", res.text, tokenJs)
                url = 'https://92722.activity-12.m.duiba.com.cn/activity/doTakePrize'
                data = f'alipay={urllib.parse.quote(self.account)}&realname={urllib.parse.quote(self.realName)}&recordId={recordId}&token={self.key_str}'
                res = requests.post(url, data=data, headers=headers)
                tx_msg = "领取失败"
                if res.status_code == 200:
                    rj = res.json()
                    tx_msg = rj["message"]
                print(
                    f"【{record['gmtCreate']}】{record['orderTypeTitle']}：{record['title']},状态：{record['statusText']}===>领取结果{tx_msg}")
            else:
                print(
                    f"【{record['gmtCreate']}】{record['orderTypeTitle']}：{record['title']},状态：{record['statusText']}")

    def run(self):
        print(f"{'-' * 20}第{self.index}个账号{'-' * 20}")
        print(f'用户【{self.name}】开始执行任务>>>')
        self.do_task()
        self.get_id()
        self.get_autologin()
        self.get_token()
        self.do_join()
        # time.sleep(10)
        self.do_take_prize()


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
    print("【版本】：20240312001")
    print("【更新内容】：更新抽奖")
    print("【TG群】：https://t.me/vhook_wool")
    accounts = getEnv("hook_yp")
    print(f"本次共发现{len(accounts)}个ck")
    push_msg = ""
    for index, env in enumerate(accounts):
        task = YongPai(index, env)
        task.run()
        time.sleep(random.randint(3, 5))
    print("所有账号执行结束>>>")
    notify.send("甬派推送", push_msg)
