

import hashlib
import json
import math
import os
import string
import time
import requests
import random
import re
from urllib.parse import quote, urlparse, parse_qs
import urllib3
from urllib.parse import parse_qs, urlsplit

urllib3.disable_warnings()

# 填wxpusher的appToken，配置在环境变量里这样没配置的账号会自动使用这个推送
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
readPostDelay = 0
if os.getenv("mykkydReadPostDelay") and os.getenv("mykkydReadPostDelay").isdecimal():
    readPostDelay = int(os.getenv("mykkydReadPostDelay"))


def push(appToken, topicIds, title, link, text, type):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "猫猫看看阅读",
        "contentType": 2,
        "topicIds": [topicIds or "11686"],
        "url": link,
    }
    # print(datapust)
    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False
    except:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        return False


def pushWechatBussiness(robotKey, link):
    datapust = {"msgtype": "text", "text": {"content": link}}
    # print(datapust)
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey
    try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")
            return True
        else:
            print("❌ 推送文章到企业微信失败！")
            return False
    except:
        print("❌ 推送文章到企业微信失败！")
        return False


def getinfo(link):
    try:
        r = requests.get(link, verify=False)
        # print(link, r.text)
        html = re.sub("\s", "", r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == "" or biz == []:
            if "__biz" in link:
                biz = re.findall("__biz=(.*?)&", link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception as e:
        # print(e)
        print("❌ 提取文章信息失败")
        return False


def ts():
    return str(int(time.time())) + "000"


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
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b8b92934da5f"],
    "MzkxNDU1NDEzNw==": ["猫猫看看服务", "gh_e50cfefef9e5"],
}


class HHYD:
    def __init__(self, cg):
        self.Cookie = cg["Cookie"]
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        global wechatBussinessKey
        self.wechatBussinessKey = wechatBussinessKey or ""
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"
        self.request_id = ""
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            # "Host": f"{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.Cookie,
        }
        self.sec = requests.session()
        self.sec.verify = False
        self.sec.headers = self.headers
        self.lastbiz = ""

    def user_info(self):
        u = f"http://{self.domnainHost}/haobaobao/user"
        r = ""
        try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get("errcode") == 0:
                print(f"账号[{self.name}]获取信息成功，用户ID为 {r.json()['data']['userid']}")
                return True
            else:
                print(f"账号[{self.name}]获取用户信息失败，账号异常 或者 Cookie无效，请检测Cookie是否正确")
                return False
        except:
            print(r.text)
            print(f"账号[{self.name}]获取用户信息失败,Cookie无效，请检测Cookie是否正确")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/haobaobao/workinfo"
            r = self.sec.get(u)
            # print(r.json())
            rj = r.json()
            self.remain_gold = math.floor(int(rj.get("data").get("remain_gold")))
            self.remain = float(rj.get("data").get("remain"))
            print(
                f'今日已经阅读了{rj.get("data").get("dayreads")}篇文章 当前金币{rj.get("data").get("remain_gold")} 当前余额{self.remain}'
            )
        except:
            print(f"账号[{self.name}]获取金币失败")
            return False

    def getKey(self):
        uk = ""
        ukRes = None
        for i in range(10):
            u = f"http://{self.domnainHost}/haobaobao/wtmpdomain"
            # print("提示 getKey：", u)
            p = f""
            r = requests.post(u, headers=self.headers, data=p, verify=False)
            # print("getKey：", r.text)
            rj = r.json()
            domain = rj.get("data").get("domain")
            # print("请求中转页：", r.text)
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            uk = pp.get("uk")[0]
            ukRes = r.text
            if uk:
                break
        if uk == "":
            print(f"账号[{self.name}]获取uk失败，返回错误：{ukRes}")
            return
        time.sleep(8)
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
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            },
            verify=False,
        )
        # print(f"账号[{self.name}] 阅读准备完成：{uk}，提取到的地址：{domain}")
        print(f"账号[{self.name}] 阅读准备成功 即将开始阅读 ✅ ，阅读参数为：{uk}")
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }
        return uk, h

    def read(self):
        info = self.getKey()
        if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return
        # print(info)
        time.sleep(2)
        arctileTime = 1
        while True:
            res = {"errcode": -1}
            refreshTime = 0
            while res["errcode"] != 0:
                timeStamp = str(ts())
                mysign = hashlib.md5(
                    (
                        info[1]["Origin"].replace("https://", "").replace("/", "")
                        + timeStamp
                        + "Lj*?Q3#pOviW"
                    ).encode()
                ).hexdigest()
                self.params = {
                    "uk": info[0],
                    "time": timeStamp,
                    "mysign": mysign,
                    "v": "3.0",
                }
                u = f"https://nsr.zsf2023e458.cloud/haobaobao/getread2"
                # print(
                #     "阅读文章参数查看：",
                #     u,
                #     self.params,
                #     info,
                #     info[1]["Origin"].replace("https://", "").replace("/", ""),
                # )
                r = requests.get(
                    u, headers=info[1], params=self.params, verify=False, timeout=60
                )
                print("-" * 50)
                # print(
                #     f"账号[{self.name}]第[{refreshTime+1}]次获取阅读文章[{info[0]}]目的页：{r.text}"
                # )
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接成功"
                    )
                else:
                    decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{decoded_str['msg']}"
                        )
                        return False
                    else:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{r.text}"
                        )
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    print(f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]超时……")
                    return
            wechatPostLink = ""
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception as e:
                    print(
                        f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                        res.get("data"),
                    )
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{returnLink}")
                    wechatPostLink = returnLink
                else:
                    # print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{wechatPostLink}")
                print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                a = getinfo(wechatPostLink)
                if a == False:
                    print(
                        f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章[{info[0]}] 失败……"
                    )
                    return False
                sleepTime = random.randint(7, 10)
                # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                if (
                    checkDict.get(a[4]) != None
                    or (res.get("data").get("a") == 2)
                    or ("&chksm=" in wechatPostLink)
                ):
                    sleepTime = readPostDelay or random.randint(15, 20)
                    print(
                        f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。"
                    )
                    if self.wechatBussinessKey:
                        pushWechatBussiness(self.wechatBussinessKey, wechatPostLink)
                    elif self.appToken:
                        push(
                            self.appToken,
                            self.topicIds,
                            "猫猫看看阅读过检测",
                            wechatPostLink,
                            f"账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 正在等待过检测，等待时间：{sleepTime}秒\n提示：快点，别耽搁时间了！",
                            "mykkyd",
                        )
                    else:
                        print(
                            f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 需要过检测，但是未配置推送token，为了避免黑号，停止阅读。。。"
                        )
                        return False
                else:
                    print(
                        f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒"
                    )
                lastestArcticleId = wechatPostLink
                self.lastbiz = a[4]
                time.sleep(sleepTime)
                u1 = f"http://nsr.zsf2023e458.cloud/haobaobao/addgolds2?time={sleepTime}&uk={info[0]}&psign={mysign}"
                r1 = requests.get(u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章"
                        )
                    except Exception as e:
                        print(
                            f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]异常：{r1.json().get('msg')}"
                        )
                        if "本次阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    print(
                        f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]失败：{r1.text}"
                    )
                    break
            elif res.get("errcode") == 405:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读重复")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读结束")
                return True
            else:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]未知情况")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):
        print(f"账号[{self.name}]开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": self.Cookie,
        }
        r = requests.get(link, headers=h, allow_redirects=False, verify=False)
        # print(r.status_code)
        Location = r.headers.get("Location")
        print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location

    def withdrawPost(self):
        u = f"http://{self.domnainHost}/haobaobao/getwithdraw"
        p = f"signid={self.request_id}&ua=0&ptype=0&paccount=&pname="
        if self.aliAccount and self.aliName:
            p = f"signid={self.request_id}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = requests.post(
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": self.Cookie,
                "Host": f"{self.domnainHost}",
                "Origin": f"http://{self.domnainHost}",
                "Proxy-Connection": "keep-alive",
                "Referer": f"http://{self.domnainHost}/haobaobao/withdraw",
                "X-Requested-With": "XMLHttpRequest",
            },
            data=p,
            verify=False,
        )
        print(f"✅ 账号[{self.name}] 提现结果：", r.json()["msg"])

    def withdraw(self):
        gold = int(int(self.remain_gold) / 1000) * 1000
        print(f"账号[{self.name}] 本次提现金额 ", self.remain, "元 ", gold, "金币")
        withdrawBalance = round((int(self.txbz) / 1000), 3)
        if gold or (self.remain >= withdrawBalance):
            if gold:
                # 开始提现
                u1 = f"http://{self.domnainHost}/haobaobao/getgold"
                p1 = f"request_id={self.request_id}&gold={gold}"
                r = requests.post(
                    u1,
                    data=p1,
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Cookie": self.Cookie,
                        "Host": f"{self.domnainHost}",
                        "Origin": f"http://{self.domnainHost}",
                        "Proxy-Connection": "keep-alive",
                        "Referer": f"http://{self.domnainHost}/haobaobao/withdraw",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    verify=False,
                )
                try:
                    res = r.json()
                    if res.get("errcode") == 0:
                        withdrawBalanceNum = self.remain + float(res["data"]["money"])
                        print(
                            f"✅ 账号[{self.name}] 金币兑换为现金成功，开始提现，预计到账 {withdrawBalanceNum} 元 >>> "
                        )

                        if withdrawBalanceNum < withdrawBalance:
                            print(f"账号[{self.name}]没有达到提现标准 {withdrawBalance} 元")
                            return False
                        self.withdrawPost()
                        return
                    else:
                        print(
                            f"账号[{self.name}] 金币兑换为现金失败：",
                            r.text,
                            " 提现地址：",
                            u1,
                            " 提现参数：",
                            p1,
                        )
                except Exception as e:
                    # raise e
                    # 处理异常
                    print(f"账号[{self.name}] 提现失败：", e)
            self.withdrawPost()

    def init(self):
        try:
            r = requests.get(
                getNewInviteUrl(),
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": self.Cookie,
                },
                verify=False,
                # 禁止重定向
                allow_redirects=False,
            )
            self.domnainHost = r.headers.get("Location").split("/")[2]
            # print(r.text)
            print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")
            # self.headers = {
            #     "Connection": "keep-alive",
            #     "Accept": "application/json, text/javascript, */*; q=0.01",
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            #     "X-Requested-With": "XMLHttpRequest",
            #     "Referer": f"http://{self.domnainHost}/",
            #     "Origin": f"http://{self.domnainHost}",
            #     # "Host": f"{self.domnainHost}",
            #     "Accept-Encoding": "gzip, deflate",
            #     "Accept-Language": "zh-CN,zh",
            #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            #     "Cookie": self.Cookie,
            # }
            # # 获取requestId
            # self.signid = ""
            # for i in range(3):
            #     r = requests.get(
            #         f"http://{self.domnainHost}/",
            #         headers={
            #             "Upgrade-Insecure-Requests": "1",
            #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            #             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            #             "Accept-Encoding": "gzip, deflate",
            #             "Accept-Language": "zh-CN,zh;q=0.9",
            #             "Cookie": self.Cookie,
            #         },
            #         verify=False,
            #     )
            #     htmltext = r.text
            #     if r.history:
            #         for resp in r.history:
            #             if "open.weixin.qq.com" in resp.headers["Location"]:
            #                 print(
            #                     f"账号[{self.name}] Cookie已过期，请重进一下网站，就会自动更新Cookie（目前不确定过期是因为自己手动进去过了还是什么其他原因）"
            #                 )
            #                 return False
            #     res1 = re.sub("\s", "", htmltext)
            #     signidl = re.findall('\)\|\|"(.*?)";', res1)
            #     # print(signidl, htmltext)
            #     if signidl == []:
            #         time.sleep(1)
            #         continue
            #     else:
            #         self.signid = signidl[0]
            #         break
            # if self.signid == "":
            #     print(f"账号[{self.name}]初始化 requestId 失败,账号异常")
            #     return False
            # # 获取提现页面地址
            r = requests.get(
                f"http://{self.domnainHost}/haobaobao/withdraw",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": self.Cookie,
                },
                verify=False,
            )
            htmltext = r.text
            signidl = re.search('request_id = "(.*?)"', htmltext)
            if signidl == []:
                print(f"账号[{self.name}]初始化 提现参数 失败，尝试另一种初始化 >>> ")
                r = requests.get(
                    f"https://code.sywjmlou.com.cn/baobaocode.php",
                    verify=False,
                )
                domnainHost = r.json()["data"]["luodi"].split("/")[2]
                r = requests.get(
                    f"http://{domnainHost}/haobaobao/withdraw",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": self.Cookie,
                    },
                    verify=False,
                )
                htmltext = r.text
                signidl = re.search('request_id = "(.*?)"', htmltext)
                if signidl == []:
                    print(f"账号[{self.name}] 多次初始化 提现参数 失败, 账号异常，请检查Cookie！")
                    r = requests.get(
                        f"https://code.sywjmlou.com.cn/baobaocode.php",
                        verify=False,
                    )
                    self.domnainHost = r.json()["data"]["luodi"].split("/")[2]
                    return False
                else:
                    self.request_id = signidl[1]
            else:
                self.request_id = signidl[1]
            return True
        except Exception as e:
            # raise e
            print(f"账号[{self.name}]初始化失败,请检查你的ck")
            return False

    def run(self):
        if self.init():
            self.user_info()
            self.gold()
            self.read()
            time.sleep(3)
            self.gold()
            time.sleep(3)
            self.withdraw()


def getNewInviteUrl():
    r = requests.get("https://code.sywjmlou.com.cn/baobaocode.php", verify=False).json()
    if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"https://s1i6.1obg.shop/haobaobao/auth/58487f291985c5f32c16b3b01b96a912".replace(
            "s1i6.1obg.shop", host or "s1i6.1obg.shop"
        )
    else:
        return "https://s1i6.1obg.shop/haobaobao/auth/58487f291985c5f32c16b3b01b96a912"


if __name__ == "__main__":
    # appToken：这个是填wxpusher的appToken
    # topicIds：这个是wxpusher的topicIds改成你自己的
    # 示例: #oZdBp04psgoN8dN1ET_uo81NTC31#3000#AT_UyIlbj2222nynESbM2vJyA7DrmUmUXD#11686
    #        "Cookie": "ejectCode=1; bbus=eyJpdiI6InZmQWFDdGIzYkNcL0tSaXB3UXl0VDlnPT0iLCJ2YWx1ZSI6IkMraGRaWDNHZmxvMUZ3Zit4U3R4MTU5b2J3ekZlTUhoTjlmck10T3JJT01kSWdYUUJnT1UwdFRKMlRvZWZCcDlkNytnYzVXMzdhT1VmUGlHcVZka2xvdGdcL2d1bnJOKzNycjRZbE9iXC9nRk1tWjNKU2NCSEk1RGpOajhORXF0TzRlWEU5MVwvQXVtRm1ubXZ1eTF1Q08zMkVvTGNZbEpaZ2pjUHc0XC90UnV2M3V6Z3JpMnMrZmlMXC9meXVPR2VNSlJVRXM1YWJWSlVSNGVZK2FpRGN0UEVPOUo2bFg4MlRJNXlKb0RDQkYyQVNFMW5RdzMyNGE1V3pNMkZQcVlORTU5T3FkQjBFUCtieDV6RTNYeHF1Ym51Z2dXQU0wc0w3eW5WRzgzUVNBcThyQnZ1NndcL1BWcWdiYVY5ZkpFdDRDbCsreUpOeUxqOVhxbjdPcXpYbVlRNU81YUZIc2g1b1huRE5CbGpSUUJTZUNJTWJwS3hJRlR6RUZjUkdoQzIzTXZ1bFhKM2RFZzNIZFEyQWhkaytIbG9DT1Zadk4zTWtKSXJrQmgwU29XQjN3WTc5WGhYdDJKdzM3cm5TaDdwd1hQQnRjY3ZjNVlwTU1BVHd3ZlNKT1grZGpaY0tOejVEdGgxYWZCeWtmaWEzdmdzYWtNUkVCWXFXYnJBZnhGYmNVWnFSTFJJK3ZPZXRNdmlURE5CZFo0Um5sbm1weHBLbDNpZ0o2XC8xQU5LSVlrRFNEbkozMlNDbkhTVVhJcnpSWjdxdDNObnZ3UlUyamZ5Z3YxYWZHWDZSWk5Vc2x2N2hxS1M1NlMxdW5nWDBDdXcxRzBudnJTaEkxSmNRME4wS04wWGVwcTlLNEUyaCtPVGFlZU1jNkdRQVk5SjJyU3VkK3JrYVEwVHhNck4rZnRsTDdqMk92V2hLVDhESG96K0lDNm9qa3pGclwvQlJ1bXB1dlNsQXlzdDNVQjdBPT0iLCJtYWMiOiI1NjI0YTczM2M5YmM3MDIwOTVmYmE0NzU5ZTc4ZWU5ZjdjMmY4MThiMmQ3ODZmODVmNGI2NjE5MTFjZTViOTg0In0%253D",

    accounts = "#ejectCode=1; bbus=eyJpdiI6InZmQWFDdGIzYkNcL0tSaXB3UXl0VDlnPT0iLCJ2YWx1ZSI6IkMraGRaWDNHZmxvMUZ3Zit4U3R4MTU5b2J3ekZlTUhoTjlmck10T3JJT01kSWdYUUJnT1UwdFRKMlRvZWZCcDlkNytnYzVXMzdhT1VmUGlHcVZka2xvdGdcL2d1bnJOKzNycjRZbE9iXC9nRk1tWjNKU2NCSEk1RGpOajhORXF0TzRlWEU5MVwvQXVtRm1ubXZ1eTF1Q08zMkVvTGNZbEpaZ2pjUHc0XC90UnV2M3V6Z3JpMnMrZmlMXC9meXVPR2VNSlJVRXM1YWJWSlVSNGVZK2FpRGN0UEVPOUo2bFg4MlRJNXlKb0RDQkYyQVNFMW5RdzMyNGE1V3pNMkZQcVlORTU5T3FkQjBFUCtieDV6RTNYeHF1Ym51Z2dXQU0wc0w3eW5WRzgzUVNBcThyQnZ1NndcL1BWcWdiYVY5ZkpFdDRDbCsreUpOeUxqOVhxbjdPcXpYbVlRNU81YUZIc2g1b1huRE5CbGpSUUJTZUNJTWJwS3hJRlR6RUZjUkdoQzIzTXZ1bFhKM2RFZzNIZFEyQWhkaytIbG9DT1Zadk4zTWtKSXJrQmgwU29XQjN3WTc5WGhYdDJKdzM3cm5TaDdwd1hQQnRjY3ZjNVlwTU1BVHd3ZlNKT1grZGpaY0tOejVEdGgxYWZCeWtmaWEzdmdzYWtNUkVCWXFXYnJBZnhGYmNVWnFSTFJJK3ZPZXRNdmlURE5CZFo0Um5sbm1weHBLbDNpZ0o2XC8xQU5LSVlrRFNEbkozMlNDbkhTVVhJcnpSWjdxdDNObnZ3UlUyamZ5Z3YxYWZHWDZSWk5Vc2x2N2hxS1M1NlMxdW5nWDBDdXcxRzBudnJTaEkxSmNRME4wS04wWGVwcTlLNEUyaCtPVGFlZU1jNkdRQVk5SjJyU3VkK3JrYVEwVHhNck4rZnRsTDdqMk92V2hLVDhESG96K0lDNm9qa3pGclwvQlJ1bXB1dlNsQXlzdDNVQjdBPT0iLCJtYWMiOiI1NjI0YTczM2M5YmM3MDIwOTVmYmE0NzU5ZTc4ZWU5ZjdjMmY4MThiMmQ3ODZmODVmNGI2NjE5MTFjZTViOTg0In0%253D#3000#AT_UyIlbj2222nynESbM2vJyA7DrmUmUXD#11686"
    inviteUrl = getNewInviteUrl()
    if accounts is None:
        print(f"你没有填入mykkyd，咋运行？\n走下邀请呗：{inviteUrl}")
    else:
        # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
        accounts_list = accounts.split("&")

        # 输出有几个账号
        num_of_accounts = len(accounts_list)
        moreTip = ""
        if readPostDelay > 0:
            moreTip = f"已设置的推送文章等待点击时间为 {readPostDelay}秒 "
        print(
            f"当前脚本版本：魔改自用版 V1.45 \n提示：获取到 {num_of_accounts} 个账号 {moreTip}\n注册地址：{inviteUrl}"
        )

        # 遍历所有账号
        for i, account in enumerate(accounts_list, start=1):
            # print("\n")
            print("-" * 50)
            print(f"账号[{account.split('#')[0]}]开始执行任务 >>>")
            # print("\n")
            # 按@符号分割当前账号的不同参数
            values = account.split("#")
            # print(values)
            cg = {}
            try:
                if len(values) == 2:
                    cg = {
                        "name": values[0],
                        "Cookie": values[1],
                        "txbz": 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }
                else:
                    cg = {
                        "name": values[0],
                        "Cookie": values[1],
                        "txbz": values[2] or 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }
            except Exception as e:
                # 处理异常
                print("逼逼叨:", "配置的啥玩意，缺参数了憨批，看清脚本说明！")
                continue
            cg["appToken"] = ""
            cg["topicIds"] = ""
            # print("手动：", len(values), values[4])
            if len(values) >= 4:
                if values[3]:
                    cg["appToken"] = values[3]
            else:
                cg["appToken"] = wxpusherAppToken
            if len(values) >= 5:
                if values[4]:
                    cg["topicIds"] = values[4]
            else:
                cg["topicIds"] = wxpusherTopicId
            if len(values) >= 6:
                if values[5]:
                    cg["aliName"] = values[5]
            if len(values) >= 7:
                if values[6]:
                    cg["aliAccount"] = values[6]
            try:
                if wechatBussinessKey == "":
                    if cg["appToken"].startswith("AT_") == False:
                        print(f"提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                        continue
                    if (cg["appToken"].startswith("AT_") == False) or (
                        cg["topicIds"].isdigit() == False
                    ):
                        print(f"提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                        continue
                api = HHYD(cg)
                if cg["aliName"] and cg["aliAccount"]:
                    print(
                        f"提示，账号[{account.split('#')[0]}] 采用了 支付宝提现，姓名：{cg['aliName']}，账户：{cg['aliAccount']}"
                    )
                else:
                    print(f"提示，账号[{account.split('#')[0]}] 采用了 微信提现")
                api.run()
            except Exception as e:
                print(
                    f"提示，账号[{account.split('#')[0]}] 出错啦，也许是平台接口问题，可以过一会尝试重新运行，如果还是不行，请将下面报错截图发到tg交流群:"
                )
                raise e
                continue
            # print("\n")
            print("-" * 50)
            print(f"账号[{account.split('#')[0]}]执行任务完毕！")
            # print("\n")
