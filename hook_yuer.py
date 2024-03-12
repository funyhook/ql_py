"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
# 反馈群：https://t.me/vhook_wool
new Env("鱼儿阅读")
cron: 9 9-21/2 * * *
反馈群：https://t.me/vhook_wool
推荐阅读 入口-> http://h5.alswywo.cn/pipa_read?upuid=1601717 (如无法打开，请复制链接在手机浏览器打开，获取最新入口)
export hook_yuer="[
    {
        'name': '不能',
        'cookie': 'PHPSESSID=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'txbz':'3000',
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
wxpusher推送配置
export wxpusher_config='{
    "wxpusher_token":"",
    "uids":["","",""],#推送到个人需要和账号数量匹配
    "topicIds":[121212,121212,121212] #推送到主题
}'
"""

import json
import logging
import os
import random
import re
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs, quote

import urllib3

urllib3.disable_warnings()

import requests

logging.basicConfig(level=logging.INFO)


class TASK:
    def __init__(self, index, ck):

        self.url = None
        self.host = None
        self.index = index
        self.cookie = ck['cookie']
        self.name = ck['name']
        self.txbz = ck['txbz']
        self.wxpusher_token = ck['wxpusher_token']
        self.wxpusher_uid = ck['wxpusher_uid']
        self.ua = 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.42.2460(0x28002A58) WeChat/arm64 Weixin NetType/WIFI Language/en ABI/arm64'
        if hasattr(ck, "User-Agent") and ck['User-Agent'] != "":
            self.ua = ck['User-Agent']
        self.logger = logging.getLogger(f"用户{self.index}")
        self.content = ''
        self.get_base_url()
        self.headers = {
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "com.tencent.mm",
            "Cookie": self.cookie
        }
        self.read_count = 0

    def log(self, msg):
        timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timeStr}-用户{self.index}【{self.name}】：{msg}")

    def get_other_url(self):
        url = 'https://qmr.bypanghu.xyz/bwjl/pp'
        add_headers = {
            'Host': 'qmr.bypanghu.xyz',
            "User-Agent": self.ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://ye1114210222-1322422422.cos.ap-nanjing.myqcloud.com/",
            "Origin": "https://ye1114210222-1322422422.cos.ap-nanjing.myqcloud.com",
            "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site"
        }
        r = requests.get(url=url, headers=add_headers)
        if r.status_code == 200:
            rt = r.text
            rj = json.loads(rt)
            url = 'http://' + urlparse(rj['jump']).netloc
            return url
        else:
            self.log("获取base_url失败,改备用的url")
            url = 'http://h5.alswywo.cn/pipa_read?upuid=1601717'
            return url

    def get_base_url(self):
        referer = self.get_other_url()
        url = 'https://h5.127-server.xyz/entry/lg'
        add_headers = {
            "Referer": referer + "/",
            "Origin": referer,
            "sec-ch-ua": '"Android WebView";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
        }

        r = requests.get(url, headers=add_headers)
        if r.status_code == 200:
            self.log("✅获取最新地址成功")
            rj = r.json()
            self.url = 'http://' + urlparse(rj['jump']).netloc
            self.host = urlparse(rj['jump']).netloc
        else:
            self.log("获取user_info_url失败,改备用的url")
            self.url = "http://h5153526.wdlvjj.bar"

    def user_info(self):
        url = self.url + '/pipa_read'
        add_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Cookie": self.cookie
        }
        res = requests.get(url, headers=add_headers)
        if not res:
            self.log("获取用户信息失败")
            return
        # print(res.text)
        match = re.search(r'ID:(\d+)', res.text)
        id = match.group(1) if match else None
        match = re.search(r'余额：(.+)</p>', res.text)
        balance = match.group(1) if match else None
        match = re.search(r'今日已读(.+)篇，', res.text)
        self.read_num = match.group(1) if match else None
        # <pstyle = "text-align: center;font-size: 3vw;color: #666" > 下一批文章将在 < bclass ="hl" > 67 < /b > 分钟后到来 < /p >
        match = re.search(r'<p[^>]*>(.*?)<b[^>]*>(.*?)</b>(.*?)</p>', res.text)
        self.limitTip = match.group(1) + match.group(2) + match.group(3) if match else None
        self.log(f"ID:{id} 余额:{balance} 今日已读{self.read_num}篇")
        time.sleep(random.randint(3, 5))

    def get_article(self):
        url1 = self.url + '/read_task/gru'
        add_headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Cookie": self.cookie
        }
        res = requests.get(url1, headers=add_headers)
        if not res:
            self.log("获取文章地址失败")
            return
        if 'jump' in res.json():
            self.log(f"✅获取文章地址成功")
            time.sleep(random.randint(3, 5))
            self.jump_location(res.json()['jump'])
        else:
            self.log(f"获取文章失败：{res.text}")

    def jump_location(self, url):
        host = urlparse(url).netloc
        headers = {
            "Host": host,
            "User-Agent": self.ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "com.tencent.mm",
        }
        urls = url + '&type=7'

        r = requests.get(urls, headers=headers)
        if r.status_code == 200:
            res = r.text
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        iu = query_parameters['iu'][0]
        url1 = f'http://{host}/read_task/do_read?iu={iu}&type=7&pageshow'
        if '加载中' in r.text:
            self.log("加载阅读文章中")
            # 获取url的iu参数
            if iu is not None:
                self.do_read(url1, url)
            else:
                self.log("获取url参数失败")
        else:
            self.log(f"加载不了")
            return

    def do_read(self, url, referer, jkey=None, retry=0):
        self.read_count += 1
        if jkey is None:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}'
        else:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}&jkey={jkey}'
        add_headers = {
            "Referer": referer + '/',
            "Origin": referer,
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "XMLHttpRequest"
        }
        requests.options(url1, headers=add_headers, )
        res = requests.get(url1, headers=add_headers)
        if res.status_code != 200 and retry ==0:
            self.log(f"第{self.read_count}次阅读失败,重试一次！")
            time.sleep(random.randint(3,6))
            self.do_read(url, referer, jkey,1)
            return
        rj = res.json()
        if 'jkey' in rj:
            if self.verify_status(rj['url']):
                pass
            else:
                return
            if 'success_msg' in res:
                self.log(f"第{self.read_count}次{rj['success_msg']}")
            else:

                self.log(f"第{self.read_count}次阅读成功")
            time.sleep(random.randint(7, 15))
            self.do_read(url, referer, rj['jkey'])
        else:
            self.log(f"本次阅读已完成,等等再来吧")

    def verify_status(self, url):
        if 'chksm=' in url:
            self.log("❗️❗️❗️出现检测文章了！")
            encoded_url = quote(url)
            self.wxpuser(url)
            self.pushAutMan("微信阅读检测【鱼儿】\n请20秒内点击下方链接", url)
            self.log("❗️❗️❗️请20秒内点击阅读啦")
            time.sleep(20)
            return True
        else:
            self.log(f"✅✅✅这次阅读没有检测")
            return True

    def with_draw(self):
        url = self.url + '/withdrawal'
        add_headers = {
            "Referer": self.url + "/new",
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Cookie": self.cookie
        }
        res = requests.get(url, headers=add_headers)
        if not res:
            self.log("获取提现信息失败")
            return
        money = re.findall(r'<span>(.*?)</span>', res.text)[0]
        balance = round(float(money) / 100, 2)
        self.log(f"当前积分{money}=={balance}元")
        if float(money) > int(self.txbz):
            self.log(f"满足提现门槛{int(self.txbz) / 100}元，开始提现")
            draw_money = round(float(money), 2)
            self.do_withdraw(draw_money)
        else:
            self.log(f"小于提现门槛{int(self.txbz) / 100}元，跳过提现")

    def do_withdraw(self, amount):
        url = self.url + '/withdrawal/submit_withdraw'
        data = f'channel=wechat&money={amount}'
        add_headers = {
            "Referer": self.url + "/withdrawal",
            "Origin": self.url,
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Host": self.host,
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Cookie": self.cookie
        }
        res = requests.post(url, data=data, headers=add_headers)
        if not res:
            self.log("提现失败")
            return
        self.log(f"提现返回结果：{res.text}")
        if res.json()['code'] == 0:
            self.log(f"提现成功")
        else:
            self.log(f"提现失败：{res}")

    def wxpuser(self, url):
        wxpusher_config = os.getenv("wxpusher_config") or ""
        if wxpusher_config and wxpusher_config != "":
            config = json.loads(wxpusher_config)
            self.wxpusher_token = config['token']
            self.wxpusher_uid = random.choice(config['uids'])
            self.log(f"本次检测推送至：{self.wxpusher_uid}")
        self.log("➡️➡️➡️开启推送至wxpusher--->")
        datapust = {
            "appToken": self.wxpusher_token,
            "content": f"""<body onload="window.location.href='{url}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{url}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n</body>""",
            "summary": "文章检测【鱼儿】",
            "contentType": 2,
            "topicIds": [],
            "uids": [self.wxpusher_uid],
            "url": url,
        }
        urlpust = "http://wxpusher.zjiecode.com/api/send/message"
        try:
            p = requests.post(url=urlpust, json=datapust, verify=False)
            if p.json()["code"] == 1000:
                self.log("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
                return True
            else:
                self.log("❌ 推送文章到微信失败，完犊子，要黑号了！")
                return False
        except:
            self.log("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False

    def pushAutMan(self, title, msg):
        autman_push_config = os.getenv("autman_push_config") or ""
        if  autman_push_config and autman_push_config == "":
            self.log("➡️➡️➡️开启推送至autman--->")
            config = json.loads(autman_push_config)
            datapust = {
                "token": config['token'],
                "plat": config['plat'],
                "groupCode": config['groupCode'],
                "userId": config['userId'],
                "title": title,
                "content": msg
            }
            try:
                p = requests.post(config['url'], data=json.dumps(datapust), headers={"Content-Type": "application/json"})
                if p.json()["ok"]:
                    self.log("✅推送文章到autman成功✅")
                else:
                    self.log(" ❗️❗️❗推送文章到autman失败❗️❗️❗")
            except Exception as e:
                self.log(f"❌ 推送文章到autman异常！！！！{e}")

    def run(self, ):
        sleepTime = random.randint(3, 5)
        print(f"降低封号风险，随机休息{sleepTime}秒")
        time.sleep(sleepTime)
        self.log(f"{'=' * 13}开始运行{'=' * 13}")
        self.get_base_url()
        self.user_info()
        if self.limitTip:
            self.log(self.limitTip)
        else:
            self.get_article()
        self.with_draw()
        self.log(f"{'=' * 13}运行结束{'=' * 13}")


def getEnv(key):  # line:343
    inviteUrl = 'http://h5.alswywo.cn/pipa_read?upuid=1601717'
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'青龙变量【{key}】没有获取到!自动退出；入口{inviteUrl}')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354
        print(f"活动入口：{inviteUrl}")


if __name__ == '__main__':
    print("【版本】：20240312001")
    print("【更新内容】：增加阅读失败，重试一次机制！")
    print("【TG群】：https://t.me/vhook_wool")
    print("【鱼儿】推荐阅读(入口)->http://h5.alswywo.cn/pipa_read?upuid=1601717")
    accounts = getEnv("hook_yuer")
    for index, ck in enumerate(accounts):
        abc = TASK(index + 1, ck)
        abc.run()
