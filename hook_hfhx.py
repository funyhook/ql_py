"""
new Env('汇丰汇选');
0 0 8 * * * hook_hfhx.py
"""
# 只有签到功能
# 反馈群：https://t.me/vhook_wool

# ck过期时间不确定
# 环境变量 hook_hfhx
# export hook_hfhx='[
#   {
#     "token":"",
#     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
#     "name":""
#   }
# ]'
# 不知道有啥用，看群友需要，练手的项目


import json
import math
import os
import time
from datetime import datetime

import execjs
import requests

hfhx_js = """
function n(n, r) {
    var t = (65535 & n) + (65535 & r);
    return (n >> 16) + (r >> 16) + (t >> 16) << 16 | 65535 & t
}
function r(r, t, e, u, o, c) {
    return n((f = n(n(t, r), n(u, c))) << (i = o) | f >>> 32 - i, e);
    var f, i
}
function t(n, t, e, u, o, c, f) {
    return r(t & e | ~t & u, n, t, o, c, f)
}
function e(n, t, e, u, o, c, f) {
    return r(t & u | e & ~u, n, t, o, c, f)
}
function u(n, t, e, u, o, c, f) {
    return r(t ^ e ^ u, n, t, o, c, f)
}
function o(n, t, e, u, o, c, f) {
    return r(e ^ (t | ~u), n, t, o, c, f)
}
function r(r, t, e, u, o, c) {
    return n((f = n(n(t, r), n(u, c))) << (i = o) | f >>> 32 - i, e);
    var f, i
}

function t(n, t, e, u, o, c, f) {
    return r(t & e | ~t & u, n, t, o, c, f)
}

function c(r, c) {
    r[c >> 5] |= 128 << c % 32,
    r[14 + (c + 64 >>> 9 << 4)] = c;
    var f, i, a, h, l, d = 1732584193, g = -271733879, v = -1732584194, s = 271733878;
    for (f = 0; f < r.length; f += 16)
        i = d,
        a = g,
        h = v,
        l = s,
        d = t(d, g, v, s, r[f], 7, -680876936),
        s = t(s, d, g, v, r[f + 1], 12, -389564586),
        v = t(v, s, d, g, r[f + 2], 17, 606105819),
        g = t(g, v, s, d, r[f + 3], 22, -1044525330),
        d = t(d, g, v, s, r[f + 4], 7, -176418897),
        s = t(s, d, g, v, r[f + 5], 12, 1200080426),
        v = t(v, s, d, g, r[f + 6], 17, -1473231341),
        g = t(g, v, s, d, r[f + 7], 22, -45705983),
        d = t(d, g, v, s, r[f + 8], 7, 1770035416),
        s = t(s, d, g, v, r[f + 9], 12, -1958414417),
        v = t(v, s, d, g, r[f + 10], 17, -42063),
        g = t(g, v, s, d, r[f + 11], 22, -1990404162),
        d = t(d, g, v, s, r[f + 12], 7, 1804603682),
        s = t(s, d, g, v, r[f + 13], 12, -40341101),
        v = t(v, s, d, g, r[f + 14], 17, -1502002290),
        d = e(d, g = t(g, v, s, d, r[f + 15], 22, 1236535329), v, s, r[f + 1], 5, -165796510),
        s = e(s, d, g, v, r[f + 6], 9, -1069501632),
        v = e(v, s, d, g, r[f + 11], 14, 643717713),
        g = e(g, v, s, d, r[f], 20, -373897302),
        d = e(d, g, v, s, r[f + 5], 5, -701558691),
        s = e(s, d, g, v, r[f + 10], 9, 38016083),
        v = e(v, s, d, g, r[f + 15], 14, -660478335),
        g = e(g, v, s, d, r[f + 4], 20, -405537848),
        d = e(d, g, v, s, r[f + 9], 5, 568446438),
        s = e(s, d, g, v, r[f + 14], 9, -1019803690),
        v = e(v, s, d, g, r[f + 3], 14, -187363961),
        g = e(g, v, s, d, r[f + 8], 20, 1163531501),
        d = e(d, g, v, s, r[f + 13], 5, -1444681467),
        s = e(s, d, g, v, r[f + 2], 9, -51403784),
        v = e(v, s, d, g, r[f + 7], 14, 1735328473),
        d = u(d, g = e(g, v, s, d, r[f + 12], 20, -1926607734), v, s, r[f + 5], 4, -378558),
        s = u(s, d, g, v, r[f + 8], 11, -2022574463),
        v = u(v, s, d, g, r[f + 11], 16, 1839030562),
        g = u(g, v, s, d, r[f + 14], 23, -35309556),
        d = u(d, g, v, s, r[f + 1], 4, -1530992060),
        s = u(s, d, g, v, r[f + 4], 11, 1272893353),
        v = u(v, s, d, g, r[f + 7], 16, -155497632),
        g = u(g, v, s, d, r[f + 10], 23, -1094730640),
        d = u(d, g, v, s, r[f + 13], 4, 681279174),
        s = u(s, d, g, v, r[f], 11, -358537222),
        v = u(v, s, d, g, r[f + 3], 16, -722521979),
        g = u(g, v, s, d, r[f + 6], 23, 76029189),
        d = u(d, g, v, s, r[f + 9], 4, -640364487),
        s = u(s, d, g, v, r[f + 12], 11, -421815835),
        v = u(v, s, d, g, r[f + 15], 16, 530742520),
        d = o(d, g = u(g, v, s, d, r[f + 2], 23, -995338651), v, s, r[f], 6, -198630844),
        s = o(s, d, g, v, r[f + 7], 10, 1126891415),
        v = o(v, s, d, g, r[f + 14], 15, -1416354905),
        g = o(g, v, s, d, r[f + 5], 21, -57434055),
        d = o(d, g, v, s, r[f + 12], 6, 1700485571),
        s = o(s, d, g, v, r[f + 3], 10, -1894986606),
        v = o(v, s, d, g, r[f + 10], 15, -1051523),
        g = o(g, v, s, d, r[f + 1], 21, -2054922799),
        d = o(d, g, v, s, r[f + 8], 6, 1873313359),
        s = o(s, d, g, v, r[f + 15], 10, -30611744),
        v = o(v, s, d, g, r[f + 6], 15, -1560198380),
        g = o(g, v, s, d, r[f + 13], 21, 1309151649),
        d = o(d, g, v, s, r[f + 4], 6, -145523070),
        s = o(s, d, g, v, r[f + 11], 10, -1120210379),
        v = o(v, s, d, g, r[f + 2], 15, 718787259),
        g = o(g, v, s, d, r[f + 9], 21, -343485551),
        d = n(d, i),
        g = n(g, a),
        v = n(v, h),
        s = n(s, l);
    return [d, g, v, s]
}
function i(n) {
    var r, t = [];
    for (t[(n.length >> 2) - 1] = void 0,
        r = 0; r < t.length; r += 1)
        t[r] = 0;
    for (r = 0; r < 8 * n.length; r += 8)
        t[r >> 5] |= (255 & n.charCodeAt(r / 8)) << r % 32;
    console.log(t);
    return t
}
function h(n) {
    return unescape(encodeURIComponent(n))
}
function f(n) {
    var r, t = "";
    for (r = 0; r < 32 * n.length; r += 8)
        t += String.fromCharCode(n[r >> 5] >>> r % 32 & 255);
    return t
}
function d(n, r) {
    return function(n, r) {
        var t, e, u = i(n), o = [], a = [];
        for (o[15] = a[15] = void 0,
        u.length > 16 && (u = c(u, 8 * n.length)),
        t = 0; t < 16; t += 1)
            o[t] = 909522486 ^ u[t],
            a[t] = 1549556828 ^ u[t];
        return e = c(o.concat(i(r)), 512 + 8 * r.length),
        f(c(a.concat(e), 640))
    }(h(n), h(r))
}


function a(n) {
    var r, t, e = "";
    for (t = 0; t < n.length; t += 1)
        r = n.charCodeAt(t),
            e += "0123456789abcdef".charAt(r >>> 4 & 15) + "0123456789abcdef".charAt(15 & r);
    return e
}

function get_token(sign1,sign2){
    var data = d(sign1,sign2)

    return a(data)
}
"""


class TASK:
    def __init__(self, i, ck):
        self.token = ck['token']
        self.name = ck['name']
        self.level = 0
        self.totalPoints = 0
        self.id = None
        self.space = ""
        self.index = i + 1
        self.ex_timeMills = math.floor(time.time() * 1000)
        self.trustToken = self.getTrustToken()
        if hasattr(ck, 'ua'):
            self.ua = ck['ua']
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        self.headers = {
            'Host': 'm.prod.app.hsbcfts.com.cn',
            'xweb_xhr': '1',
            'XHSBCE2ETrustToken': self.trustToken,
            'calltiming': str(self.ex_timeMills),
            'platform': 'pinf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090926) XWEB/8555',
            'auth-Token': self.token,
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wxe13c5e6eb2f24313/66/page-frame.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getTrustToken(self):
        print(self.space)
        ctx = execjs.compile(hfhx_js)
        return ctx.call('get_token', 'wechat-sign', 'wechat-sign' + str(self.ex_timeMills))

    def sign(self):
        url = 'https://m.prod.app.hsbcfts.com.cn/wechat/pwcs/wechat/pinnacle/pinfmp/usertask/signIn'
        response = requests.post(url=url, headers=self.headers, data=None)
        if response.status_code == 200:
            rj = response.json()
            if rj['code'] == 0:
                print(f"用户【{self.name}】签到结果：签到成功！")
                print(f"用户【{self.name}】当前积分：{rj['data']['res']['rewardPointsValue']}")
                print(f"用户【{self.name}】签到天数：{rj['data']['res']['consecutiveSignInDays']} 天")
            elif rj['code'] == 401:
                print(f"用户【{self.name}】token失效，请重新抓包！！！")
            else:
                print(f"用户【{self.name}】签到结果：{rj['message']}")
                self.getUserInfo()

    def getUserInfo(self):
        url = 'https://m.prod.app.hsbcfts.com.cn/wechat/pwcs/wechat/pinnacle/pinfmp/usertask/index'
        data = {
            "defaultCount": 4
        }
        response = requests.post(url=url, headers=self.headers, json=data)
        if response.status_code == 200:
            rj = response.json()
            if rj['code'] == 0:
                print(f"用户【{self.name}】当前积分：{rj['data']['pointsInfo']['pointBalance']}")
                print(f"用户【{self.name}】签到天数：{rj['data']['pointsInfo']['signInDaysOfMonth']} 天")
                return True
            elif rj['code'] == 401:
                print(f"用户【{self.name}】token失效，请重新抓包！！！")
            else:
                print(f"用户【{self.name}】签到结果：{rj['message']}")
        return False

    def run(self):
        print(f"{'-' * 20}第{self.index}个账号{'-' * 20}")
        print(f'用户【{self.name}】开始执行任务>>>')
        self.sign()


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
    accounts = getEnv("hook_hfhx")
    # accounts = [
    #     {
    #         "token": "13f7d9fcec0984a469a8c336b21654639",
    #         "name": "ls"
    #     },
    # ]
    for i, env in enumerate(accounts):
        task = TASK(i, env)
        task.run()
