"""
# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 反馈群：https://t.me/vhook_wool
* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* https://osk17500.vsdfrgj0986.top:10252/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2
* 打开活动入口，抓包的任意接口cookies中的Cookie参数

* 变量
export hook_mmkk='[
    {
        "name": "ls",
        "Cookie": "=1; bbus=%253D",
        "txbz": 3000,
        "aliAccount": "",
        "aliName": "",
        "appToken": "",
        "topicIds": ""
    },
]'

* autman 推送配置
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

cron: 0 */25 8-22 * * *
new Env('猫猫看看');
"""
import asyncio
import hashlib
import json
import math
import multiprocessing
import os
import random
import re
import time
from datetime import datetime
from urllib.parse import parse_qs
from urllib.parse import quote, urlparse

import requests
import urllib3

import notify

urllib3.disable_warnings()
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""


def push(appToken, topicIds, title, link, text, type):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "猫猫看看阅读",
        "contentType": type,
        "topicIds": [int(topicIds)],
        "url": link,
    }

    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False
    except:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        return False


async def pushWechatBussiness(link):
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


async def pushAutMan(title, msg):
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
    def __init__(self, i, cg):
        self.inviteUrl = None
        self.remain = None
        self.Cookie = cg["Cookie"]
        self.index = i + 1
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
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
        self.datTimeformat = '%Y-%m-%d %H:%M:%S'

    def ts(self):
        return str(int(time.time())) + "000"

    def timeStr(self):
        return datetime.now().strftime(self.datTimeformat)

    def log(self, msg):
        print(f"用户{self.index}【{self.name}】：{msg}")

    def user_info(self):
        u = f"http://{self.domnainHost}/haobaobao/user"
        r = ""
        try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get("errcode") == 0:
                self.log(f"获取信息成功，用户ID为 {r.json()['data']['userid']}")
                return True
            else:
                self.log("获取用户信息失败，账号异常 或者 Cookie无效，请检测Cookie是否正确")
                return False
        except:
            self.log("获取用户信息失败,Cookie无效，请检测Cookie是否正确")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/haobaobao/workinfo"
            r = self.sec.get(u)
            rj = r.json()
            self.remain_gold = math.floor(int(rj.get("data").get("remain_gold")))
            self.remain = float(rj.get("data").get("remain"))
            content = f'【账号】：{self.name} \n今日阅读：{rj.get("data").get("dayreads")}篇｜当前金币：{rj.get("data").get("remain_gold")}个｜当前余额：{self.remain}元'
            self.log(
                f'今日已经阅读了{rj.get("data").get("dayreads")}篇文章 当前金币{rj.get("data").get("remain_gold")} 当前余额{self.remain}')
            return content
        except:
            self.log("获取金币失败")
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
            if not domain:
                return None
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            uk = pp.get("uk")[0]
            ukRes = r.text
            if uk:
                break
        if uk == "":
            self.log("获取uk失败，返回错误：{ukRes}")
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }
        return uk, h

    def getinfo(self,link):
        try:
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
            return nickname, user_name, msg_title, text, biz
        except Exception as e:
            self.log(f"提取文章信息失败❌ {e}")
            return False

    def read(self):
        info = self.getKey()
        if not info:
            return
        if len(info) == 0:
            self.log("获取阅读参数失败，停止往后阅读！⚠️ ")
            return
        # print(info)
        time.sleep(2)
        arctileTime = 1
        while True:
            res = {"errcode": -1}
            refreshTime = 0
            while res["errcode"] != 0:
                timeStamp = str(self.ts())
                mysign = hashlib.md5((info[1]["Origin"].replace("https://", "").replace("/",
                                                                                        "") + timeStamp + "Lj*?Q3#pOviW").encode()).hexdigest()
                self.params = {
                    "uk": info[0],
                    "time": timeStamp,
                    "mysign": mysign,
                    "v": "3.0",
                }
                u = f"https://nsr.zsf2023e458.cloud/haobaobao/getread2"
                r = requests.get(u, headers=info[1], params=self.params, verify=False, timeout=60)
                # print("-" * 50)
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    self.log(f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章跳转链接成功")
                else:
                    decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:
                        self.log(
                            f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章跳转链接失败：{decoded_str['msg']}")
                        return False
                    else:
                        self.log(f"第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章跳转链接失败：{r.text}")
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    self.log(f"⚠️获取阅读第[{arctileTime}]篇文章超时……")
                    return
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception as e:
                    self.log(
                        f"⚠️ 获取阅读第[{arctileTime}]篇文章链接失败，疑似台子接口太垃圾，崩了，返回数据为：{res.get('data')}")
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    self.log(f" 阅读第[{arctileTime}]篇微信文章")
                    wechatPostLink = returnLink
                else:
                    # self.log(" 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    self.log(f"阅读第[{arctileTime}]篇微信文章")
                self.log(f"阅读第[{arctileTime}]篇文章")
                a = self.getinfo(wechatPostLink)
                if not a:
                    self.log(f"⚠️ 因获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章 失败……")
                    return False
                sleepTime = random.randint(7, 10)
                # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                if checkDict.get(a[4]) is not None or (res.get("data").get("a") == 2) or ("&chksm=" in wechatPostLink):
                    sleepTime = random.randint(15, 20)
                    self.log(
                        f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。")
                    asyncio.run(pushAutMan('阅读检测推送【猫猫看看】',
                                           f"快点下方链接\n{wechatPostLink}\n等待时间：{sleepTime}秒 ,别耽搁时间了"))
                    asyncio.run(pushWechatBussiness(wechatPostLink))
                    if self.appToken:
                        push(
                            self.appToken,
                            self.topicIds,
                            "猫猫看看阅读过检测",
                            wechatPostLink,
                            f"账号[{self.name}]阅读第[{arctileTime}]篇文章 正在等待过检测，等待时间：{sleepTime}秒\n提示：快点，别耽搁时间了！",
                            2,
                        )
                else:
                    self.log(f"✅阅读第[{arctileTime}]篇文章 非检测文章，模拟读{sleepTime}秒")
                lastestArcticleId = wechatPostLink
                self.lastbiz = a[4]
                time.sleep(sleepTime)
                u1 = f"http://nsr.zsf2023e458.cloud/haobaobao/addgolds2?time={sleepTime}&uk={info[0]}&psign={mysign}"
                r1 = requests.get(u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:
                        self.log(
                            f"✅ 阅读第[{arctileTime}]篇文章所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章")
                    except Exception as e:
                        self.log(f"❌阅读第[{arctileTime}]篇文章异常：{r1.json().get('msg')}")
                        if "本次阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    self.log(f"❌ 阅读第[{arctileTime}]篇文章失败：{r1.text}")
                    break
            elif res.get("errcode") == 405:
                self.log(f"⚠️ 阅读第[{arctileTime}]篇文章阅读重复")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                self.log(f"⚠️ 阅读第[{arctileTime}]篇文章阅读结束")
                return True
            else:
                self.log(f"⚠️ 阅读第[{arctileTime}]篇文章未知情况")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):
        self.log("开始本次阅读……")
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
        self.log("开始阅读文章 - {Location}")
        return Location

    def withdrawPost(self):
        u = f"http://{self.domnainHost}/haobaobao/getwithdraw"
        p = f"signid={self.request_id}&ua=0&ptype=0&paccount=&pname="
        header = {
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
        }
        if self.aliAccount and self.aliName:
            p = f"signid={self.request_id}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = requests.post(u, headers=header, data=p, verify=False)
        if r.json()['errcode'] == 0:
            self.log(f"✅ 提现结果：", r.json()['msg'])
        elif "上限" in r.json()['msg']:
            self.log(f"⚠️ 默认提现方式达到上限，一分钟后自动切换第二种提现方式")
            time.sleep(60)
            self.aliAccount = None
            self.aliName = None
            self.init()
            self.withdrawPost()
        else:
            self.log(f"❌ 提现失败：", r.json()['msg'])

    def goldCharge(self):
        gold = int(int(self.remain_gold) / 1000) * 1000
        header = {
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
        }
        if gold:
            # 开始兑换余额
            u1 = f"http://{self.domnainHost}/haobaobao/getgold"
            p1 = f"request_id={self.request_id}&gold={gold}"
            r = requests.post(u1, data=p1, headers=header, verify=False)
            try:
                res = r.json()
                if res.get("errcode") == 0:
                    withdrawBalanceNum = self.remain + float(res["data"]["money"])
                    return withdrawBalanceNum
                else:
                    self.log(f"❌金币兑换为现金失败：{r.text}")
            except Exception as e:
                self.log(f"❌兑换余额失败：{e}")

    def withdraw(self):
        gold = int(int(self.remain_gold) / 1000) * 1000
        withdrawBalance = round((int(self.txbz) / 1000), 3)
        if gold:
            self.remain = self.goldCharge()
        self.log(f"本次提现金额 {self.remain}元，{gold}金币,提现门槛：{withdrawBalance}元")
        if self.remain >= withdrawBalance:
            self.log(f"✅满足提现门槛 {withdrawBalance} 元，开始提现>>>")
            self.withdrawPost()
        else:
            self.log(f"❌没有达到提现标准 {withdrawBalance} 元")

    def init(self):
        headers = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.Cookie,
        }
        try:
            r = requests.get(self.getNewInviteUrl(), headers=headers, verify=False, allow_redirects=False)
            self.domnainHost = r.headers.get("Location").split("/")[2]
            # print(r.text)
            self.log(f"提取到的域名：{self.domnainHost}")
            # 获取提现页面地址
            r = requests.get(f"http://{self.domnainHost}/haobaobao/withdraw", headers=headers, verify=False, )
            htmltext = r.text
            signidl = re.search('request_id = "(.*?)"', htmltext)
            if signidl == []:
                self.log("初始化 提现参数 失败，尝试另一种初始化 >>> ")
                r = requests.get(f"https://code.sywjmlou.com.cn/baobaocode.php", verify=False)
                domnainHost = r.json()["data"]["luodi"].split("/")[2]
                r = requests.get(f"http://{domnainHost}/haobaobao/withdraw", headers=headers, verify=False)
                htmltext = r.text
                signidl = re.search('request_id = "(.*?)"', htmltext)
                if not signidl:
                    self.log(" 多次初始化 提现参数 失败, 账号异常，请检查Cookie！")
                    r = requests.get(f"https://code.sywjmlou.com.cn/baobaocode.php", verify=False, )
                    self.domnainHost = r.json()["data"]["luodi"].split("/")[2]
                    return False
                else:
                    self.request_id = signidl[1]
            else:
                self.request_id = signidl[1]
            return True
        except Exception as e:
            # raise e
            self.log("初始化失败,请检查你的ck")
            return False

    def getNewInviteUrl(self):
        r = requests.get("https://code.sywjmlou.com.cn/baobaocode.php", verify=False).json()
        if r.get("code") == 0:
            newEntryUrl = r.get("data").get("luodi")
            parsed_url = urlparse(newEntryUrl)
            host = parsed_url.hostname
            self.inviteUrl = f"https://s1i6.1obg.shop/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2".replace(
                "s1i6.1obg.shop", host or "s1i6.1obg.shop")
        else:
            self.inviteUrl = "https://s1i6.1obg.shop/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2"
        return self.inviteUrl

    def run(self):
        run_msg =''
        self.log(f"{'=' * 13}{self.timeStr()}开始运行{'=' * 13}")
        if self.init():
            self.user_info()
            self.gold()
            self.read()
            time.sleep(2)
            run_msg = self.gold()
            time.sleep(1)
            self.withdraw()
        self.log(f"{'=' * 13}{self.timeStr()}运行结束{'=' * 13}")
        return run_msg



def getEnv(key):  # line:343
    inviteUrl = 'https://osk17500.vsdfrgj0986.top:10252/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2'
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


def process_account(i, ck):
    read = HHYD(i, ck)
    return read.run()


if __name__ == "__main__":
    print("【猫猫看看】阅读入口：https://osk17500.vsdfrgj0986.top:10252/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2")
    accounts = getEnv("hook_mmkk")

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
    # notify.send("[猫猫看看阅读推送]", push_msg)
    for index, account in enumerate(accounts):
        push_msg += f"\n{'-' * 50}\n"
        push_msg += process_account(index, account)
    notify.send("[猫猫看看阅读推送]", push_msg)
