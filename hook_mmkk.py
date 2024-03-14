"""
* 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
* 反馈群：https://t.me/vhook_wool
* 版本：2024-03-12（更新算法）
* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* https://osk17500.vsdfrgj0986.top:10252/haobaobao/auth/20fac27802e2f2eee23f8804de20c1c2
*
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
new Env('猫猫看看阅读');
"""
import hashlib
import json
import math
import os
import random
import re
import time
from datetime import datetime
from urllib.parse import parse_qs
from urllib.parse import quote, urlparse

import requests
import urllib3

from utils import notify, common

urllib3.disable_warnings()

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
    "MzkxNDU1NDEzNw==": ["猫猫看看服务", "gh_e50cfefef9e5"],
}

mykkydDetectingSealStatus = True
mykkydDisabledDetectingSealSetting = os.getenv("mykkydDisabledDetectingSeal")
if mykkydDisabledDetectingSealSetting not in ["", None]:
    if mykkydDisabledDetectingSealSetting in ["1", "true", True]:
        mykkydDetectingSealStatus = False


def extract_middle_text(source, before_text, after_text, all_matches=False):
    results = []
    start_index = source.find(before_text)

    while start_index != -1:
        source_after_before_text = source[start_index + len(before_text):]
        end_index = source_after_before_text.find(after_text)

        if end_index == -1:
            break

        results.append(source_after_before_text[:end_index])
        if not all_matches:
            break

        source = source_after_before_text[end_index + len(after_text):]
        start_index = source.find(before_text)

    return results if all_matches else results[0] if results else ""


class HHYD:
    def __init__(self, i, account):
        self.readJumpPath = None
        self.inviteUrl = None
        self.remain = None
        self.index = i + 1
        self.name = account["name"]
        self.Cookie = account["Cookie"]
        self.txbz = account.get("txbz", 30)
        self.topicIds = account.get("topicIds", "")
        self.appToken = account.get("appToken", "")
        self.wxpusher_token = account.get("wxpusher_token",None)
        self.wxpusher_uid = account.get("wxpusher_uid",None)
        self.aliAccount = account.get("aliAccount", None)
        self.aliName = account.get("aliName", None)
        self.ua = "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.42.2460(0x28002A58) WeChat/arm64 Weixin NetType/WIFI Language/en ABI/arm64"
        self.ua = account.get("User-Agent",self.ua)
        self.domnainHost = "1698855139.hxiong.top"
        self.request_id = ""
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": self.ua,
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
            content = f'【{self.name}】已读：{rj.get("data").get("dayreads")}篇 金币：{rj.get("data").get("remain_gold")}个 余额：{self.remain}元'
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
                "User-Agent": self.ua,
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
            "User-Agent": self.ua,
        }
        return uk, h

    def getinfo(self, link):
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
                mysign = hashlib.md5(
                    (info[1]["Host"] + timeStamp + "Lj*?Q3#pOviW").encode()
                ).hexdigest()
                self.params = {
                    "uk": info[0],
                    "time": timeStamp,
                    "mysign": mysign,
                    "v": "4.0",
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
                    wechatPostLink = returnLink
                else:
                    # self.log("阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                self.log(f"阅读第[{arctileTime}]篇微信文章")
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
                    self.wxpuser(wechatPostLink)
                    self.pushAutMan('阅读检测推送【猫猫看看】',
                                    f"快点下方链接\n{wechatPostLink}\n等待时间：{sleepTime}秒 ,别耽搁时间了")
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
            "User-Agent": self.ua,
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
            "User-Agent": self.ua,
        }
        if self.aliAccount and self.aliName:
            p = f"signid={self.request_id}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = requests.post(u, headers=header, data=p, verify=False)
        if r.json()['errcode'] == 0:
            self.log(f"✅ 提现结果：{r.json()['msg']}", )
        elif "上限" in r.json()['msg']:
            self.log(f"⚠️ 默认提现方式达到上限，一分钟后自动切换第二种提现方式")
            time.sleep(60)
            self.aliAccount = None
            self.aliName = None
            self.init()
            self.withdrawPost()
        else:
            self.log(f"❌ 提现失败：{r.json()['msg']}", )

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
            "User-Agent": self.ua,
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
        try:
            r = requests.get(
                self.getNewInviteUrl(),
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
            self.log(f"提取到的域名：{self.domnainHost}")
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
            self.readJumpPath = ""
            if mykkydDetectingSealStatus:
                r = requests.get(
                    f"http://{self.domnainHost}/haobaobao/home",
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
                read_jump_read_text = extract_middle_text(
                    htmltext, "function read_jump_read(){", "success: function"
                )
                if read_jump_read_text:
                    readJumpPath = extract_middle_text(
                        read_jump_read_text, "url: domain+'", "',"
                    )
                    if readJumpPath:
                        self.readJumpPath = readJumpPath
                    else:
                        self.log(f"初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ ")
                        return False
                else:
                    if "存在违规操作" in htmltext:
                        self.log(f"被检测到了，已经被封，终止任务，快去提醒大家吧~ ")
                        exit(0)
                    else:
                        self.log(f"初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ ")
                        return False
            else:
                self.readJumpPath = "/haobaobao/wtmpdomain2"
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
                self.log(f"初始化 提现参数 失败，尝试另一种初始化 >>> ")
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
                    self.log(f"多次初始化 提现参数 失败, 账号异常，请检查Cookie！")
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
            self.log(f"初始化失败,请检查你的ck")
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

    def wxpuser(self, url):
        wxpusher_config = os.getenv("wxpusher_config") or ""
        if wxpusher_config and wxpusher_config != "":
            config = json.loads(wxpusher_config)
            self.wxpusher_token = config['token']
            self.wxpusher_uid = random.choice(config['uids'])
        self.log(f"➡️wxpusher-推送至-->{self.wxpusher_uid}")

        datapust = {
            "appToken": self.wxpusher_token,
            "content": f"""<body onload="window.location.href='{url}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{url}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n</body>""",
            "summary": "文章检测【猫猫看看】",
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
        if  autman_push_config and autman_push_config != "":
            self.log("👉️👉️👉️开启推送至autman--->")
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
        self.log(f"{'=' * 13}{self.timeStr()}开始运行{'=' * 13}")
        sleepTime = random.randint(3, 5)
        self.log(f"降低封号风险，随机休息{sleepTime}秒")
        time.sleep(sleepTime)
        if self.init():
            self.user_info()
            self.gold()
            self.read()
            time.sleep(2)
            run_msg = self.gold()
            time.sleep(1)
            self.withdraw()
        self.log(f"{'=' * 13}{self.timeStr()}运行结束{'=' * 13}\n")
        return run_msg


def process_account(i, ck):
    read = HHYD(i, ck)
    return read.run()


def getEnv(key):  # line:343
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'\n青龙变量【{key}】没有获取到!自动退出')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        print(f"\n----------共获取到{len(env_str)}个账号----------\n")
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354


if __name__ == "__main__":
    common.check_cloud("hook_mmkk", 1.1)
    accounts = getEnv("hook_mmkk")

    push_msg = ""
    for index, account in enumerate(accounts):
        push_msg += f"\n{'-' * 50}\n"
        push_msg += process_account(index, account)
    notify.send("[猫猫看看阅读推送]", push_msg)
