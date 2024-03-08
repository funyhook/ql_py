"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
走不走邀请都无所谓了,能走更好,不走也没关系,我的要求,
请勿擅自修改脚本注释,
请勿将脚本擅自分享传播至任何地方,请勿将邀请更改为自己的邀请拉取人头,
如果你这样做了,我是没办法怎么样你的
阅读：可乐阅读
new Env("可乐阅读")
cron: 9 9-21/2 * * *
反馈群：https://t.me/vhook_wool
走邀请:推荐阅读 -> http://44521803081319.cfgwozp.cn/r?upuid=445218
(如无法打开，请复制链接在手机浏览器打开，获取最新入口)
export hook_klyd="[
    {
        'name': '不能',
        'cookie': 'PHPSESSID=; udtauth3=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181',
        'wxpusher_token': '',
        'wxpusher_uid': ''
    }
]"

autman 推送配置
export autman_push_config='{
    "url":"http://ip:port/push",
    "token":"自定义token",
    "plat":"wb",
    "userId":"用户ID",
    "groupCode":"群号"
}'
"""

import asyncio
import json
import logging
import os
import random
import time
from typing import Optional, Dict
from urllib.parse import urlparse, parse_qs, quote

import aiohttp

logging.basicConfig(level=logging.INFO)


class TASK:
    def __init__(self, index, ck):
        self.index = index
        self.cookie = ck['cookie']
        self.name = ck['name']
        self.wxpusher_token = ck['wxpusher_token']
        self.wxpusher_uid = ck['wxpusher_uid']
        self.ua = 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.42.2460(0x28002A58) WeChat/arm64 Weixin NetType/WIFI Language/en ABI/arm64'
        if hasattr(ck, "ua") and ck['ua'] != "":
            self.ua = ck['ua']
        self.sessions = aiohttp.ClientSession()
        self.logger = logging.getLogger(f"用户{self.index}")
        self.content = ''

    def log(self, msg):  # 改写一下日志
        print(f"用户{self.index}｜{self.name}:{msg}")
        # self.content += str(msg) + '\n'

    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None,
                      dtype='json'):
        host = urlparse(url).netloc
        _default_headers = {
            "Host": host,
            "User-Agent": self.ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "X-Requested-With": "com.tencent.mm",
            "Cookie": self.cookie
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            async with getattr(self.sessions, method)(url, headers=request_headers, data=data) as response:
                if response.status == 200:
                    if dtype == 'json':
                        return await response.json()
                    else:
                        return await response.text()
                else:
                    self.log(f"请求失败状态码：{response.status}")
                    # 可以选择休眠一段时间再重试，以避免频繁请求
                    await asyncio.sleep(random.randint(3, 5))  # 休眠1秒钟
        except Exception as e:
            self.log(f"请求出现错误：{e}")
            await asyncio.sleep(random.randint(3, 5))  # 休眠1秒钟

    async def get_base_url(self):
        url = 'http://44521803071743.emoxtvg.cn/r?upuid=445218'
        host = urlparse(url).netloc
        add_headers = {
            'Host': host,
            "User-Agent": self.ua,
            "Accept": "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        async with self.sessions.get(url, headers=add_headers, allow_redirects=False) as response:
            if response.status == 302:
                url = response.headers.get('Location')
                # print(self.url)
                self.url = 'http://' + urlparse(url).netloc
            else:
                self.log("获取base_url失败,改备用的url")
                self.url = 'http://m224482.ww1112017.cn'

    async def user_info(self):
        url = self.url + '/tuijian'
        add_headers = {
            "Referer": self.url + "/new",
        }
        res = await self.request(url, add_headers=add_headers)
        if not res:
            self.log("获取用户信息失败")
            return
        if res['code'] == 0:
            self.log(
                f"{res['data']['user']['username']} uid:{res['data']['user']['uid']}, 积分{res['data']['user']['score']},已阅读{res['data']['infoView']['num']}篇")
            if 'msg' in res['data']['infoView']:
                self.log(f"提示：{res['data']['infoView']['msg']}")
                return False
            self.read_num = int(res['data']['infoView']['num'])

            return True
        else:
            self.log(f"获取用户信息失败：{res}")

    async def get_article(self):

        url = self.url + '/new/get_read_url'
        add_headers = {
            "Referer": self.url + "/new?upuid=445218",
        }
        res = await self.request(url, add_headers=add_headers, dtype='text')
        if not res:
            self.log("获取文章失败")
            return
        if 'jump' in res:
            res = json.loads(res)
            # self.log(f"jump 文章地址：{res['jump']}")
            # 获取当前小时数
            # now_num = int(time.strftime('%H', time.localtime()))
            # if self.read_num < 2:
            #     self.log("🤡🤡🤡,今天还没手动阅读，推送是过不了的，结束该账户任务")
            #     return
            # if now_num in [12,13,14]:
            #     self.log("🤡🤡🤡,现在是中下午，推荐手动阅读或者等待3点后，如不需要请注释脚本153，154，155行")
            #     return
            # await self.wxpuser(f"可乐阅读[用户{self.index}]请90秒阅读2-3篇过检测", quote(url))
            # self.log("请90秒内读文章2-3篇,没过就算了,我就在原地死等90秒!!!!")
            # start_time = int(time.time())
            # while True:
            #     if await self.get_read_state():
            #         self.log(f"👌👌👌你已经打开了阅读链接,请耐心的阅读2-3篇文章")
            #         break
            #     if int(time.time())- start_time > 90:
            #         self.log(f"😓😓😓90秒到啦,本次阅读你放弃了,下次再来")
            #         return
            # end_time = int(time.time())
            # await asyncio.sleep((start_time+90)-end_time)
            await self.jump_location(res['jump'])
        else:
            self.log(f"获取文章失败：{res}")

    async def jump_location(self, url):
        host = urlparse(url).netloc
        # print("jump_location:: " + url)
        headers = {
            "Host": host,
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        # async with self.sessions.get(url,headers=headers, allow_redirects=False) as response:
        #     print(response.headers)
        #     if response.status == 302:
        #         # 获取响应头里的set-cookie
        #         location = response.headers.get('Location')
        #     else:
        #         self.logger.error(f'获取重定向地址失败，状态码：{response.status}')
        #         return
        add_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}

        res1 = await self.request(url, add_headers=add_headers, dtype='text')
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        iu = query_parameters['iu'][0]
        url1 = 'http://' + parsed_url.netloc + f'/tuijian/do_read?for=&zs=&pageshow='
        if '加载中' in res1:
            self.log("加载阅读文章中")
            # 获取url的iu参数
            if iu is not None:
                await asyncio.sleep(random.randint(2, 3))
                await self.do_read(url1, iu, url)
            else:
                self.log("获取url参数失败")
        else:
            self.log(f"加载不了")
            return

    async def do_read(self, url, iu, referer, jkey=None, ):
        if jkey is None:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}&iu={iu}'
        else:
            url1 = url + f'&r={round(random.uniform(0, 1), 16)}&iu={iu}&jkey={jkey}'
        add_headers = {
            "Referer": referer,
            "X-Requested-With": "XMLHttpRequest"
        }
        res = await self.request(url1, add_headers=add_headers)
        # print(f"doread::: {res}")
        if not res or not res['url']:
            self.log("阅读失败,请稍后再试试")
            return
        if res['url'] != 'close' and 'jkey' in res:
            if 'success_msg' in res:
                self.log(f"{res['success_msg']}")
            else:
                self.log(f"阅读成功")
            if await self.verify_status(res['url']):
                pass
            else:
                return
            await asyncio.sleep(random.randint(6, 12))
            await self.do_read(url, iu, referer, res['jkey'])
        else:
            self.log(f"{res}")

    async def verify_status(self, url):
        if 'chksm' in url:
            self.log("⚠️⚠️⚠️⚠️⚠️出现检测文章了！")
            encoded_url = quote(url)
            await self.wxpuser(encoded_url)
            await self.pushAutMan("微信阅读渐次【可乐】",encoded_url)
            self.log("⚠️⚠️⚠️请20秒内点击阅读啦")
            time.sleep(20)
            return True
        else:
            self.log(f"✅这次阅读没有检测")
            return True

    async def with_draw(self):
        url = self.url + '/withdrawal'
        add_headers = {
            "Referer": self.url + "/new",
        }
        res = await self.request(url, add_headers=add_headers)
        if not res:
            self.log("获取提现信息失败")
            return
        if res['code'] == 0:
            self.log(
                f"{res['data']['user']['username']}当前积分{res['data']['user']['score']}=={round(float(res['data']['user']['score']) / 100, 2)}元")
            tag = 60
            if float(res['data']['user']['score']) > tag:
                draw_money = int(float(res['data']['user']['score']))
                await self.do_withdraw(draw_money)
        else:
            self.log(f"获取提现信息失败：{res}")
            return

    async def do_withdraw(self, amount):
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
        res = await self.request(url, 'post', data=data, add_headers=add_headers, dtype='text')
        if not res:
            self.log("提现失败")
            return
        # self.log(res)
        if '"code":0' in res:
            self.log(f"提现成功")
        else:
            self.log(f"提现失败：{res}")

    async def wxpuser(self, url):
        content = "检测文章-可乐%0A请在90秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27link%27%22%3E"
        content = content.replace('link', url)
        wxpuser_url = f'https://wxpusher.zjiecode.com/demo/send/custom/{self.wxpusher_uid}?content={content}'
        res = await self.request(wxpuser_url, 'get', headers={"Content-Type": "application/json"})
        if res['success'] == True:
            self.log(f"[通知]--->检测发送成功！")
        else:
            self.log(f"[通知]====>发送失败！！！！！")

    async def pushAutMan(self,title, msg):
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
            p = await self.request(config['url'], "post",data=datapust,headers=None)
            if p.json()["ok"]:
                print("✅ ⚠️推送文章到autman成功！⚠️")
                return True
            else:
                print("❌ 推送文章到autman失败！")
                return False
        except:
            print("❌ 推送文章到autman失败！")
            return False

    async def run(self,):
        sleepTime = self.index-1 * random.randint(10,15)
        await asyncio.sleep(sleepTime)
        await self.get_base_url()
        self.log(f"{'=' * 13}开始运行{'=' * 13}")
        if await self.user_info():
            await self.get_article()
        await self.with_draw()
        self.log(f"{'=' * 13}运行结束{'=' * 13}")
        await self.close()


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


async def main():
    accounts = getEnv("hook_klyd")
    for index, ck in enumerate(accounts):
        abc = TASK(index + 1, ck)
        await abc.run()


if __name__ == '__main__':
    print("推荐阅读(入口)->http://44521803081319.cfgwozp.cn/r?upuid=445218")
    asyncio.run(main())
