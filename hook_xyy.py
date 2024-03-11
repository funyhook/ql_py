"""
cron: 30 */30 8-22 * * *
new Env('小阅阅阅读');
* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* https://osl4.f4135.shop/yunonline/v1/auth/c5c3f97ce3894f1c08593c4a6c54dbfe?codeurl=osl4.f4135.shop&codeuserid=2&time=1709089052
* 打开活动入口，抓包的任意接口cookies中的Cookie参数
* 反馈群：https://t.me/vhook_wool
* 变量
export hook_xyy='[
    {
        "name": "ls",
        "ysm_uid": "",
        "unionId": "",
        "txbz": 3000,
        "aliAccount": "",
        "aliName": "",
        "appToken": "",
        "topicIds": ""
    },
]'
*autman 推送配置
export autman_push_config='{
    "url":"http://ip:port/push",
    "token":"自定义token",
    "plat":"wb",
    "userId":"用户ID",
    "groupCode":"群号"
}'
* 定时运行每半小时一次
* 达到标准自动提现
* 达到标准，自动提现

"""
import hashlib
import json
import math
import multiprocessing
import os
import random
import re
import time
from urllib.parse import parse_qs, urlsplit
from urllib.parse import quote, urlparse

import requests
import urllib3

import notify

urllib3.disable_warnings()


def push(appToken, topicIds, title, link, text, type):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "小阅阅阅读",
        "contentType": type,
        "topicIds": [int(topicIds)],
        "url": link,
    }

    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:  # line:59:try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True  # line:64:return True
        else:  # line:65:else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")  # line:66:print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False  # line:67:return False
    except:  # line:68:except:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")  # line:69:print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        return False  # line:70:return False


def pushWechatBussiness(link):
    wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
    if not wechatBussinessKey:
        return
    datapust = {"msgtype": "text", "text": {"content": link}}
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + wechatBussinessKey
    try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")
            return True
        else:  # line:83:else:
            print("❌ 推送文章到企业微信失败！")
            return False
    except:
        print("❌ 推送文章到企业微信失败！")
        return False


def pushAutMan(title, msg):
    autman_push_config = os.getenv("autman_push_config") or ""
    if not autman_push_config or autman_push_config == "":
        print("❌ 推送文章到autman失败！")
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
    try:
        p = requests.post(url=config['url'], json=datapust, verify=False)
        if p.json()["ok"]:
            print("✅ ⚠️推送文章到autman成功！⚠️")
            return True
        else:
            print("❌ 推送文章到autman失败！")
            return False
    except:
        print("❌ 推送文章到autman失败！")
        return False


def getNewInviteUrl():  # line:594:def getNewInviteUrl():
    r = requests.get("https://www.filesmej.cn/waidomain.php", verify=False).json()
    if r.get("code") == 0:  # line:596:if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709089052".replace(
            "u7ds.sy673.shop", host or "u7ds.sy673.shop"
        )  # line:602:)
    else:  # line:603:else:
        return "https://osl4.f4135.shop/yunonline/v1/auth/c5c3f97ce3894f1c08593c4a6c54dbfe?codeurl=osl4.f4135.shop&codeuserid=2&time=1709089052"  # line:604:return "https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176"


def getEnv(key):  # line:343
    inviteUrl = getNewInviteUrl()
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'【{key}】青龙变量里没有获取到!自动退出；入口{inviteUrl}')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354
        print(f"活动入口：{inviteUrl}")


def ts():  # line:122:def ts():
    return (
            str(int(time.time())) + "000"
    )  # line:123:return str(int(time.time())) + "000"


checkDict = {
    "MzkxNTE3MzQ4MQ==": ["香姐爱旅行", "gh_54a65dc60039"],
    "Mzg5MjM0MDEwNw==": ["我本非凡", "gh_46b076903473"],
    "MzUzODY4NzE2OQ==": ["多肉葡萄2020", "gh_b3d79cd1e1b5"],
    "MzkyMjE3MzYxMg==": ["Youhful", "gh_b3d79cd1e1b5"],
    "MzkxNjMwNDIzOA==": ["少年没有乌托邦3", "gh_b3d79cd1e1b5"],
    "Mzg3NzUxMjc5Mg==": ["星星诺言", "gh_b3d79cd1e1b5"],
    "Mzg4NTcwODE1NA==": ["斑马还没睡123", "gh_b3d79cd1e1b5"],
    "Mzk0ODIxODE4OQ==": ["持家妙招宝典", "gh_b3d79cd1e1b5"],
    "Mzg2NjUyMjI1NA==": ["Lilinng", "gh_b3d79cd1e1b5"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b3d79cd1e1b5"],
    "Mzg5ODUyMzYzMQ==": ["789也不行", "gh_b3d79cd1e1b5"],
    "MzU0NzI5Mjc4OQ==": ["皮蛋瘦肉猪", "gh_58d7ee593b86"],
    "Mzg5MDgxODAzMg==": ["北北小助手", "gh_58d7ee593b86"],
    "MzkxNDU1NDEzNw==": ["小阅阅服务", "gh_e50cfefef9e5"],
}  # line:142:}


class HHYD:  # line:145:class HHYD:
    def __init__(self, i, cg):
        self.shoutu_balance = 0
        self.unionId = cg["unionId"]
        self.ysm_uid = cg["ysm_uid"]
        self.index = i + 1
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        self.wxpusher_token = cg['wxpusher_token']
        self.wxpusher_uid = cg['wxpusher_uid']
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"
        self.exchangeParams = ""
        self.ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.8.7(0x1308070c) XWEB/1191 Flue'
        if hasattr(cg, "User-Agent") and cg['User-Agent'] != "":
            self.ua = cg['User-Agent']
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": self.ua,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"ysm_uid={self.ysm_uid};",
        }  # line:172:}
        self.sec = requests.session()
        self.sec.verify = False  # line:174:self.sec.verify = False
        self.sec.headers = self.headers
        self.lastbiz = ""  # line:176:self.lastbiz = ""

    def log(self, msg):
        print(f"用户{self.index}【{self.name}】：{msg}")

    def getinfo(self, link):
        try:  # line:92:try:
            r = requests.get(link, verify=False)
            html = re.sub("\s", "", r.text)
            biz = re.findall('varbiz="(.*?)"\|\|', html)
            if biz:
                biz = biz[0]
            if biz == "" or biz == []:
                if "__biz" in link:
                    biz = re.findall("__biz=(.*?)&", link)
                    if biz:
                        biz = biz[0]
            nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
            if nickname:
                nickname = nickname[0]
            user_name = re.findall('varuser_name="(.*?)";', html)
            if user_name:
                user_name = user_name[0]
            msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
            if msg_title:
                msg_title = msg_title[0]
            text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
            # self.log(text)
            return nickname, user_name, msg_title, text, biz
        except Exception as e:  # line:116:except Exception as e:
            self.log("❌ 提取文章信息失败")  # line:118:print("❌ 提取文章信息失败")
            return False  # line:119:return False

    def user_info(self):  # line:178:def user_info(self):
        u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"
        r = ""
        try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get("errcode") == 0:
                self.log(f"获取信息成功，当前阅读文章每篇奖励 {r.json()['data']['award']}个金币")  # line:187:)
                return True
            else:
                self.log(f"获取用户信息失败，账号异常 或者 ysm_uid无效，请检测ysm_uid是否正确")
                return False
        except:
            print(r.text)
            self.log(f"获取用户信息失败,ysm_uid无效，请检测ysm_uid是否正确")
            return False

    def hasWechat(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/hasWechat?unionid={self.unionId}"
            r = self.sec.get(u)
            self.log(f"判断公众号任务数量：{r.json()['data']['has']}")
        except:  # line:203:except:
            self.log(f"判断是否有公众号任务失败：{r.text}")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/gold?unionid={self.unionId}&time={ts()}"
            r = self.sec.get(u)
            rj = r.json()
            self.remain = math.floor(int(rj.get("data").get("last_gold")))
            content = f'【账号】：{self.name} \n今日阅读：{rj.get("data").get("day_read")}篇｜当前金币：{rj.get("data").get("last_gold")}个，账户余额：{self.shoutu_balance}元'
            self.log(
                f'今日已经阅读了{rj.get("data").get("day_read")}篇文章,剩余{rj.get("data").get("remain_read")}未阅读，今日获取金币{rj.get("data").get("day_gold")}，剩余{self.remain}')
            return content
        except:
            self.log(f"账号[{self.name}]获取金币失败")
            return False

    def getKey(self):
        uk = ""
        ukRes = None
        for i in range(10):
            u = f"http://{self.domnainHost}/yunonline/v1/wtmpdomain"
            p = f"unionid={self.unionId}"
            r = requests.post(u, headers=self.headers, data=p, verify=False)
            rj = r.json()
            domain = rj.get("data").get("domain")
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            uk = pp.get("uk")[0]
            ukRes = r.text
            if uk:
                break
        if uk == "":
            self.log(f"获取uk失败，返回错误：{ukRes}")
            return
        time.sleep(8)  # line:243:time.sleep(8)
        r = requests.get(
            domain,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": f"{hn}",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": self.ua,
            },
            verify=False,
        )  # line:260:)
        self.log(f"阅读准备成功 即将开始阅读 ✅ ，阅读参数为：{uk}")
        h = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "nsr.zsf2023e458.cloud",
            "Origin": f"https://{hn}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": self.ua,
        }  # line:274:}
        return uk, h  # line:275:return uk, h

    def read(self):  # line:277:def read(self):
        info = self.getKey()  # line:278:info = self.getKey()
        if len(info) == 0:  # line:279:if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return  # line:281:return
        time.sleep(2)  # line:283:time.sleep(2)
        arctileTime = 1  # line:284:arctileTime = 1
        lastestArcticleId = ""  # line:285: = ""
        while True:  # line:286:while True:
            res = {"errcode": -1}  # line:287:res = {"errcode": -1}
            refreshTime = 0  # line:288:refreshTime = 0
            while (
                    res["errcode"] != 0
            ):  # line:289:while res["errcode"] != 0:
                timeStamp = str(ts())  # line:290:timeStamp = str(ts())
                psgn = hashlib.md5(
                    (
                            info[1]["Origin"].replace("https://", "")[:11]
                            + info[0]
                            + timeStamp
                            + "A&I25LILIYDS$"
                    ).encode()
                ).hexdigest()
                self.params = {"uk": info[0], "time": timeStamp, "psgn": psgn}
                u = f"https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"
                r = requests.get(u, headers=info[1], params=self.params, verify=False, timeout=60, )
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    self.log(f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章，跳转链接成功")
                else:
                    decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:
                        self.log(
                            f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章，跳转链接失败：{decoded_str['msg']}")
                        return False
                    else:
                        self.log(f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章，跳转链接失败：{r.text}")
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    self.log(f" 获取阅读第[{arctileTime}]篇文章，超时……⚠️")
                    return
            wechatPostLink = ""
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception as e:
                    self.log(
                        f"获取阅读第[{arctileTime}]篇文章，链接失败，疑似台子接口太垃圾，崩了⚠️，返回数据为：{res.get('data')}")
                    continue  # line:340:continue
                if "mp.weixin.qq.com" in returnLink:
                    self.log(f"阅读第[{arctileTime}]篇微信文章")
                    wechatPostLink = returnLink
                else:
                    wechatPostLink = self.jump(returnLink)
                self.log(f"阅读第[{arctileTime}]篇文章")
                a = self.getinfo(wechatPostLink)
                if not a:
                    self.log(f"因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章， ⚠️ 失败……")  # line:353:)
                    return False
                sleepTime = random.randint(7, 10)
                if checkDict.get(a[4]) is not None or (lastestArcticleId == wechatPostLink) or (
                        "&chksm=" in wechatPostLink):
                    sleepTime = random.randint(15, 20)
                    self.log(
                        f"阅读第[{arctileTime}]篇文章， 检测到疑似检测文章⚠️ ，正在推送，等待过检测，等待时间：{sleepTime}秒。。。")
                    self.wxpuser(wechatPostLink)
                    self.pushAutMan('阅读检测【小阅阅】',
                                    f"快点下方链接\n{wechatPostLink}\n等待时间：{sleepTime}秒 ,别耽搁时间了")

                else:
                    self.log(f"阅读第[{arctileTime}]篇文章， 非检测文章✅，模拟读{sleepTime}秒")
                lastestArcticleId = wechatPostLink
                self.lastbiz = a[4]
                time.sleep(random.randint(15, 30))
                u1 = f"http://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={info[0]}&time={sleepTime}&timestamp={ts()}"
                r1 = requests.get(u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:  # line:392:try:
                        self.log(
                            f"阅读第[{arctileTime}]篇文章，所得金币✅ ：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章")  # line:395:)
                    except Exception as e:
                        self.log(f"阅读第[{arctileTime}]篇文章，异常❌ ：{r1.json().get('msg')}")
                        if "本次阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    self.log(f"阅读第[{arctileTime}]篇文章，失败❌ ：{r1.text}")
                    break
            elif res.get("errcode") == 405:
                self.log(f"阅读第[{arctileTime}]篇文章，阅读重复⚠️ ")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                self.log(f"阅读第[{arctileTime}]篇文章，阅读结束⚠️ ")
                return True
            else:
                self.log(f"阅读第[{arctileTime}]篇文章，未知情况⚠️")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):
        self.log(f"开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": f"ysm_uid={self.ysm_uid}",
        }  # line:432:}
        r = requests.get(link, headers=h, allow_redirects=False, verify=False)
        Location = r.headers.get("Location")
        self.log(f"开始阅读文章 - {Location}")  # line:436:print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location  # line:437:return Location

    def withdraw(self):
        if int(self.remain) >= 3000:
            gold = int(int(self.remain) / 1000) * 1000
            query = urlsplit(self.exchangeParams).query
            exchangeParams = parse_qs(query)  # line:447:
            for key, value in exchangeParams.items():
                exchangeParams[key] = value[0]
            u1 = f"http://{self.domnainHost}/yunonline/v1/user_gold"
            p1 = f"unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&gold={gold}"
            r = requests.post(
                u1,
                data=p1,
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                    "Host": f"{self.domnainHost}",
                    "Origin": f"http://{self.domnainHost}",
                    "Proxy-Connection": "keep-alive",
                    "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange{self.exchangeParams}",
                    "User-Agent": self.ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                verify=False,
            )
            try:
                res = r.json()
                if res.get("errcode") == 0:
                    self.log(f"✅兑换金币成功=>{gold}={int(self.remain) / 10000}元")
            except Exception as e:
                self.log(f"提现失败❌：{r.text}")
        do_tixian = False
        if int(self.remain) < int(self.txbz):
            do_tixian = False
        if float(self.shoutu_balance) > 0 and float(self.shoutu_balance) * 1000 < int(self.txbz):
            do_tixian = True
        if do_tixian:
            self.do_withDraw()
        else:
            self.log(f"❗️未达到提现门槛{int(self.txbz) / 10000}元，跳过提现")

    def do_withDraw(self):
        query = urlsplit(self.exchangeParams).query
        exchangeParams = parse_qs(query)
        for key, value in exchangeParams.items():
            exchangeParams[key] = value[0]
        u = f"http://{self.domnainHost}/yunonline/v1/withdraw"
        p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=0&paccount=&pname="
        if self.aliAccount and self.aliName:
            p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"ysmuid={self.ysm_uid}",
            "Host": f"{self.domnainHost}",
            "Origin": f"http://{self.domnainHost}",
            "Proxy-Connection": "keep-alive",
            "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange?{self.exchangeParams}",
            "User-Agent": self.ua,
            "X-Requested-With": "XMLHttpRequest"
        }
        r = requests.post(u, headers=headers, data=p, verify=False)
        if r.status_code == 200:
            rj = r.json()
            self.log(f"✅提现成功:{rj['msg']}")
        else:
            self.log(f"提现结果❌{r.text}")

    def init(self):
        try:
            res = requests.get(
                "https://nsr.zsf2023e458.cloud/yunonline/v1/getchatsite?t=1709019551&cid=785d878cb1e76a31cc1b52224d935ab7&code=081ktRFa1TM60H0gr4Ga1U6Pc10ktRFX&state=1",
                verify=False,
            )
            self.domnainHost = res.json()["data"]["luodi"].split("/")[2]
            self.log(f"提取到的域名：{self.domnainHost}")
            self.headers = {
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": self.ua,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"http://{self.domnainHost}/",
                "Origin": f"http://{self.domnainHost}",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysm_uid={self.ysm_uid};",
            }
            self.signid = ""
            for index in range(10):
                res = requests.get(
                    f"http://{self.domnainHost}/",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": self.ua,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": f"ysmuid={self.ysm_uid}",
                    },
                    verify=False,
                )
                htmltext = res.text
                res1 = re.sub("\s", "", htmltext)
                shoutu_balance_match = re.findall(r'<div class="num number rewardNum">(\d+\.\d+)</div>', htmltext)
                if shoutu_balance_match:
                    self.shoutu_balance = shoutu_balance_match[0]
                self.log(f"账户余额：{self.shoutu_balance}元")
                signidl = re.findall('\)\|\|"(.*?)";', res1)
                if not signidl:
                    continue
                else:
                    self.signid = signidl[0]
                    break
            if self.signid == "":
                self.log(f"初始化 requestId 失败,账号异常❌")
                return False  # line:553:return False
            res = requests.get(
                f"http://{self.domnainHost}/?cate=0",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": self.ua,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": f"ysmuid={self.ysm_uid}",
                },
                verify=False,
            )
            htmltext = res.text
            res1 = re.sub("\s", "", htmltext)
            signidl = re.findall('/yunonline/v1/exchange(.*?)"', res1)
            if not signidl:
                self.log(f"初始化 提现参数 失败,账号异常")
                return False
            else:
                self.exchangeParams = signidl[0]
            return True
        except Exception as e:
            self.log(f"初始化失败,请检查你的ck:{e}")
            return False

    def wxpuser(self, url):
        datapust = {
            "appToken": self.wxpusher_token,
            "content": f"""<body onload="window.location.href='{url}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{url}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n</body>""",
            "summary": "文章检测【可乐】",
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
        if not autman_push_config or autman_push_config == "":
            self.log("未配置autman推送，跳过推送autman！")
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
        try:
            p = requests.post(config['url'], data=json.dumps(datapust), headers={"Content-Type": "application/json"})
            if p.json()["ok"]:
                self.log("✅推送文章到autman成功✅")
            else:
                self.log(" ❗️❗️❗推送文章到autman失败❗️❗️❗")
        except Exception as e:
            self.log(f"❌ 推送文章到autman异常！！！！{e}")

    def run(self):
        run_msg = ''
        print(f"{'+' * 20}开始第{self.index}个账号{'+' * 20}")
        if self.init():
            self.user_info()
            self.hasWechat()
            self.gold()
            self.read()
            time.sleep(3)
            run_msg = self.gold()
            time.sleep(3)
            self.withdraw()
        return run_msg


def process_account(i, ck):
    read = HHYD(i, ck)
    return read.run()


if __name__ == "__main__":
    print(
        "【小阅阅】 推荐阅读(入口)->https://osl4.f4135.shop/yunonline/v1/auth/c5c3f97ce3894f1c08593c4a6c54dbfe?codeurl=osl4.f4135.shop&codeuserid=2&time=1709089052")
    accounts = getEnv("hook_xyy")
    print(f'******共获取到{len(accounts)}个账号******')
    # 获取CPU核心数量
    num_cores = multiprocessing.cpu_count()
    print(f'系统CPU核心数量为: {num_cores},开始并发任务！')
    # 根据CPU核心数量设置进程数量
    num_processes = num_cores
    push_msg = ''
    # 使用进程池执行
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    #     # 将每个账号的处理作为一个任务提交给进程池
    #     # 这将导致所有任务并行执行
    #     futures = [executor.submit(process_account, index, account, push_msg) for index, account in enumerate(accounts)]
    #     # 等待所有任务完成
    #     concurrent.futures.wait(futures)
    #     notify.send("[小阅阅推送]", push_msg)
    for index, account in enumerate(accounts):
        push_msg += f"\n{'-' * 50}\n"
        push_msg += process_account(index, account)
    notify.send("[小阅阅阅读推送]", push_msg)
