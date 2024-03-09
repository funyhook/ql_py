"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
# 反馈群：https://t.me/vhook_wool
阅读：可乐阅读
new Env("可乐阅读")
cron: 9 9-21/2 * * *
反馈群：https://t.me/vhook_wool
走邀请:推荐阅读 -> http://44521803081319.cfgwozp.cn/r?upuid=445218 (如无法打开，请复制链接在手机浏览器打开，获取最新入口)

export hook_klyd="[
    {
        'name': '不能',
        'cookie': 'PHPSESSID=; udtauth3=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': '',
        'wxpusher_uid': ''
    }
]"

autman 推送配置 需要市场安装【消息推送API】插件
export autman_push_config='{
    "url":"http://ip:port/push",
    "token":"自定义token",
    "plat":"wb",
    "userId":"用户ID",
    "groupCode":"群号"
}'
"""

import json
import logging
import os
import random
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs, quote

import requests

logging.basicConfig(level=logging.INFO)


class TASK:
    def __init__(self, index, ck):
        self.index = index
        self.cookie = ck['cookie']
        self.name = ck['name']
        self.wxpusher_token = ck['wxpusher_token']
        self.wxpusher_uid = ck['wxpusher_uid']
        self.ua = 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.42.2460(0x28002A58) WeChat/arm64 Weixin NetType/WIFI Language/en ABI/arm64'
        if hasattr(ck, "User-Agent") and ck['User-Agent'] != "":
            self.ua = ck['User-Agent']
        self.sessions = requests.session()
        self.logger = logging.getLogger(f"用户{self.index}")
        self.content = ''
        self.read_count = 0

    def log(self, msg):  # 改写一下日志
        timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timeStr}-用户{self.index}【{self.name}】：{msg}")

    def close(self):
        self.sessions.close()

    def get_base_url(self):
        url = 'http://44521803071743.emoxtvg.cn/r?upuid=445218'
        host = urlparse(url).netloc
        add_headers = {
            'Host': host,
            "User-Agent": self.ua,
            "Accept": "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        with self.sessions.get(url, headers=add_headers, allow_redirects=False) as response:
            if response.status_code == 302:
                url = response.headers.get('Location')
                # print(self.url)
                self.url = 'http://' + urlparse(url).netloc
            else:
                self.log("获取base_url失败,改备用的url")
                self.url = 'http://m224482.ww1112017.cn'

    def user_info(self):
        try:
            url = self.url + '/tuijian'
            host = urlparse(url).netloc
            headers = {
                "Referer": self.url + "/new",
                "Host": host,
                "User-Agent": self.ua,
                "Cookie": self.cookie,
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "X-Requested-With": "com.tencent.mm",
            }
            res = requests.get(url, headers=headers)
            if not res:
                self.log("获取用户信息失败")
                return
            rj = res.json()
            if rj['code'] == 0:
                self.log(
                    f"{rj['data']['user']['username']} uid:{rj['data']['user']['uid']}, 积分{rj['data']['user']['score']},已阅读{rj['data']['infoView']['num']}篇")
                if 'msg' in rj['data']['infoView']:
                    self.log(f"提示：{rj['data']['infoView']['msg']}")
                    return False
                self.read_num = int(rj['data']['infoView']['num'])

                return True
            else:
                self.log(f"获取用户信息失败：{res}")
        except Exception as e:
            self.log(f"获取用户信息失败：")
            return False

    def get_article(self):
        url = self.url + '/new/get_read_url'
        host = urlparse(url).netloc
        headers = {
            "Referer": self.url + "/new?upuid=445218",
            "Host": host,
            "User-Agent": self.ua,
            "Cookie": self.cookie,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "com.tencent.mm",

        }
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            self.log("获取文章失败")
            return
        rj = res.json()
        if 'jump' in rj:
            self.jump_location(rj['jump'])
        else:
            self.log(f"获取文章失败：{res.text}")

    def jump_location(self, url):
        host = urlparse(url).netloc
        headers = {
            "Host": host,
            "User-Agent": self.ua,
            "Cookie": self.cookie,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "com.tencent.mm",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}

        res1 = requests.get(url, headers=headers)
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        iu = query_parameters['iu'][0]
        url1 = 'http://' + parsed_url.netloc + f'/tuijian/do_read?for=&zs=&pageshow='
        if '加载中' in res1.text:
            self.log("加载阅读文章中")
            # 获取url的iu参数
            if iu is not None:
                time.sleep(random.randint(2, 3))
                self.do_read(url1, iu, url)
            else:
                self.log("获取url参数失败")
        else:
            self.log(f"加载不了")
            return

    def do_read(self, url, iu, referer, jkey=None, ):
        self.read_count += 1
        if jkey is None:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}&iu={iu}'
        else:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}&iu={iu}&jkey={jkey}'
        host = urlparse(url).netloc
        headers = {
            "Referer": referer,
            "Host": host,
            "User-Agent": self.ua,
            "Cookie": self.cookie,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "XMLHttpRequest"

        }
        res = requests.get(url1, headers=headers)
        print(f"doread::: {res.text}")
        if not res or not res.json()['url']:
            self.log(f"第{self.read_count}次阅读失败,请稍后再试试")
            return
        if res.json()['url'] != 'close' and 'jkey' in res:
            if 'success_msg' in res:
                self.log(f"第{self.read_count}次：{res.json()['success_msg']}")
            else:
                self.log(f"第{self.read_count}次阅读成功")
            if self.verify_status(res.json()['url']):
                pass
            else:
                return
            time.sleep(random.randint(6, 12))
            self.do_read(url, iu, referer, res.json()['jkey'])
        else:
            self.log(f"{res.text}")

    def verify_status(self, url):
        if 'chksm' in url:
            self.log(f"第{self.read_count}次️出现检测文章了❗️❗️❗️❗")
            encoded_url = quote(url)
            self.wxpuser(encoded_url)
            self.pushAutMan("微信阅读检测【可乐】\n请20秒内点击下方链接", url)
            self.log(f"第{self.read_count}次️ ️请20秒内点击阅读啦❗️❗️❗")
            time.sleep(20)
            return True
        else:
            self.log(f"第{self.read_count}次️ 这次阅读没有检测✅")
            return True

    def with_draw(self):
        url = self.url + '/withdrawal'
        host = urlparse(url).netloc
        add_headers = {
            "Referer": self.url + "/new",
            "Host": host,
            "User-Agent": self.ua,
            "Cookie": self.cookie,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "XMLHttpRequest"

        }
        res = requests.get(url, headers=add_headers)
        if not res:
            self.log("获取提现信息失败")
            return
        rj = res.json()
        if rj['code'] == 0:
            self.log(
                f"{rj['data']['user']['username']}当前积分{rj['data']['user']['score']}=={round(float(rj['data']['user']['score']) / 100, 2)}元")
            tag = 60
            if float(rj['data']['user']['score']) > tag:
                draw_money = int(float(rj['data']['user']['score']))
                self.do_withdraw(draw_money)
        else:
            self.log(f"获取提现信息失败：{res.text}")
            return

    def do_withdraw(self, amount):
        url = self.url + '/withdrawal/doWithdraw'
        # data = f'amount={amount}&type=wx'
        data = {
            'amount': amount,
            'type': 'wx'
        }
        add_headers = {
            "Referer": self.url + "/new",
            "Origin": self.url,
            "X-Requested-With": "XMLHttpRequest"
        }
        res = requests.post(url, data=data, headers=add_headers)
        if not res:
            self.log("提现失败")
            return
        # self.log(res)
        if '"code":0' in res:
            self.log(f"提现成功")
        else:
            self.log(f"提现失败：{res}")

    def wxpuser(self, url):
        content = "检测文章-可乐%0A请在90秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27link%27%22%3E"
        content = content.replace('link', url)
        wxpuser_url = f'https://wxpusher.zjiecode.com/demo/send/custom/{self.wxpusher_uid}?content={content}'
        res = requests.get(wxpuser_url, headers={"Content-Type": "application/json"})
        if res.json()['success']:
            self.log(f"第{self.read_count}次，[通知]--->检测发送成功！✅")
        else:
            self.log(f"第{self.read_count}次，[通知]====>发送失败❌")

    def pushAutMan(self, title, msg):
        autman_push_config = os.getenv("autman_push_config") or ""
        if not autman_push_config or autman_push_config == "":
            self.log(f"第{self.read_count}次，推送文章到autman失败！")
            return
        config = json.loads(autman_push_config)
        datapust = {
            "token": config['token'],
            "plat": config['plat'],
            "groupCode": config['groupCode'],
            "userId": config['userId'],
            "title": title,
            "content": msg
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:

            p = requests.post(config['url'], data=json.dumps(datapust), headers=headers)
            if p.json()["ok"]:
                self.log(f"第{self.read_count}次，推送文章到autman成功✅")
            else:
                self.log(f"第{self.read_count}次，推送文章到autman失败😭😭😭")
        except Exception as e:
            self.log(f"第{self.read_count}次，推送文章到autman异常️❗️❗{e}")

    def run(self, ):
        sleepTime = random.randint(3, 5)
        print(f"降低封控，休息{sleepTime}秒")
        # time.sleep(sleepTime)
        self.get_base_url()
        self.log(f"{'=' * 13}开始运行{'=' * 13}")
        if self.user_info():
            self.get_article()
            self.with_draw()
        self.log(f"{'=' * 13}运行结束{'=' * 13}")


def getEnv(key):  # line:343`
    inviteUrl = 'http://44521803071743.emoxtvg.cn/r?upuid=445218'
    env_str = os.getenv(key)
    if env_str is None:
        print(f'【{key}】青龙变量里没有获取到!自动退出；入口{inviteUrl}')
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确 {e}')  # line:354
        print(f"活动入口：{inviteUrl}")


if __name__ == '__main__':
    print("【可乐】推荐阅读(入口)->http://44521803081319.cfgwozp.cn/r?upuid=445218")
    # accounts = getEnv("hook_klyd")
    accounts = [
    {
        'name': '不能',
        'cookie': 'PHPSESSID=s7icv23bskcdqb175vb47ca9af; udtauth3=83dftG0lf3y%2F7TIzjWImkEIFDUqhiX2pRIewS%2BrBrPhcPtlm6iO%2BWxeaDql0WmEsqdX8BalGIYWc70iVmezDLYeXlq3yivWQhRakvP0oEGPGzmtGX1HiPrKhG6te6jAzcbFhNDPy99joVQgTcO3asRLurce6UENbPgAob2lpleM',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    },{
        'name': 'shao',
        'cookie': 'PHPSESSID=919pu86a2h20milvh9l0ps7veh; udtauth3=8a51OhwEqEhSEBuHwbvDc%2BSfkSI5i6%2FUwrybkJY%2B%2B6QIWPHisxbIdzK8hCqysVDw5clwd1nKqcl1QEnIKYzapLMDNNfRS%2BX1lThPFuqgGFDp3VqHkGbgp3ItIC2xIeut7D0AtHvWxYkSBbzdIOAO03jswJV5PSp8JhYBQIRR%2BP0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    },{
        'name': 'xuer',
        'cookie': 'udtauth3=3848lGMk1vMicRL9pTlsc0CW0mBQTYBxNlZdwIgJTYfNYPv5Rvd%2F0J9Sz913J%2FpZtEdoYRWip8tYq0iIpLMgDHbJQGw4gBbqwhidlJ6q18%2B0XnGE0M4QZiCBbx60FH%2FCXzf%2BIoAEuGPtqwwy%2FIMse5CJOlIeQpm2Ln2%2BqS3FwEo; PHPSESSID=lh0u0it9d171d9ealeg8rm59g7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    },
    {
        'name': 'v-java',
        'cookie': 'udtauth3=6b32fe6%2FFQfBcUOe4wreZ3jJAw5ygdbJQW02ygjYtYc1G%2BNODvQ5u6p7hfkXA1ZNkUCQMPSSnMBWqZDkFbTWF6ILsUefb%2BBHoV9uLJbaib2P4LnI1QYasCiACbgBNbNyXzf0gOZ3xYzbByK2h1xUp%2FuZh%2FD90Z2wCbgrVEWCKF8; PHPSESSID=1igh43o10retmsq3lkkjqnmd4t',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    },
    {
        'name': 'vx-635623451',
        'cookie': 'udtauth3=9f40uGY1Q9d0me7wkq6hfGEmGQE9Bf%2B9ZgcYrs9IQ2gx81bB7LvwPgg9iTSoZ4CATa1lVv3mp2L3YolsVnuFHixNn4LfX92PaDZPl8samq17su5Pafdsorb4qYe%2FwcOj04o5G7jCSRcn76iKUsgpsqtHbOzbLMIjycKZabaJEEc; PHPSESSID=qongcrkqssjg6rlbrl0eu9phd9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    },
    {
        'name': 'v-181209',
        'cookie': 'udtauth3=0a3b9%2FcVi%2B3x5%2BE%2F4ngzSp5XDMlb5cdzQPyeg7mgpiio%2FkhptOIXv5MekXjxmpBc%2BTIv1wUodfqfrg81%2BAywAcOx9UB5d2%2BnQzPneVxT3aiQNdUw48VMwQufOmXuzfblC1wQW7DhbOUxgZpknoN%2Fu6jHHB5FN9gnVQxUOFFKk%2F4; PHPSESSID=dlp8lh5oud44t91el2vk4rs7nk',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': 'AT_9QMHP2jfb733ObTbxXFA3ZsrFTz0xtPR',
        'wxpusher_uid': 'UID_rDaUycMDJ7RZJaPEnpJdhXMcI2yl'
    }
]
    for index, ck in enumerate(accounts):
        abc = TASK(index + 1, ck)
        abc.run()
