oo0o = '''
cron: 30 */30 8-22 * * *
new Env('f可乐阅读');
# 反馈群：https://t.me/vhook_wool

活动入口：http://44521803071743.emoxtvg.cn/r?upuid=445218

使用方法：
1.入口,WX打开：http://44521803071743.emoxtvg.cn/r?upuid=445218

'''  # line:7
'''
1.入口,WX打开http://44521803071743.emoxtvg.cn/r?upuid=445218

若链接微信无法打开，请复制到浏览器复制新链接打开
2.打开活动入口，抓包的任意接口cookie参数
3.青龙配置文件，添加本脚本环境变量
填写变量参数时为方便填写可以随意换行
单账户：export klydconfig="[{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'}]"
多账户：export klydconfig="[
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'},
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'},
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'}
]"
参数说明：
name:备注名随意填写
cookie:打开活动入口，抓包的任意接口headers中的cookie参数
key：每个账号的推送标准，每个账号全阅读只需要一个key,多个账号需要多个key,key永不过期。
为了防止恶意调用key接口，限制每个ip每天只能获取一个key。手机开飞行模式10s左右可以变更ip重新获取key
通过浏览器打开链接获取:http://175.24.153.42:8882/getkey
uids:wxpusher的参数，当一个微信关注了一个wxpusher的推送应用后，会在推送管理后台(https://wxpusher.zjiecode.com/admin/main)的'用户管理-->用户列表'中显示
用户在推送页面点击’我的-->我的UID‘也可以获取
User-Agent:抓包任意接口在headers中看到
4.青龙环境变量菜单，添加本脚wxpusher环境变量(不需要重复添加)
建议使用方式二
方式一：青龙添加环境变量参数 ：
名称 ：push_config
参数 ：{"printf":0,"threadingf":1,"threadingt":3,"appToken":"xxxx"}
方式二：配置文件添加
export push_config="{'printf':0,'threadingf':1,'threadingt':3,'appToken':'xxxx'}"
参数说明：
printf:0是不打印调试日志，1是打印调试日志
threadingf:并行运行账号参数 1并行执行，0顺序执行，并行执行优点，能够并行跑所以账号，加快完成时间，缺点日志打印混乱。
threadingt:并行运行时每个账号的间隔时间默认3s
appToken 这个是填wxpusher的appToken,找不到自己百度

5.本地电脑python运行
在本脚本最下方代码if __name__ == '__main__':下填写
例如
loc_push_config={"printf":0,"threadingf":1,"threadingt":3,"appToken":"xxxx"}
loc_klydconfig=[
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'},
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'},
{'name':'备注名','cookie': 'PHPSESSID=xxxx; udtauth3=a267Rxxxxx','key':'xxxxxxx','uids':'xxxxxxx'}
]
6.在本脚本最下方代码if __name__ == '__main__':下配置UA变量
User-Agent参数可以抓包任意接口在headers中看到
定时运行每半个小时一次
'''  # line:54

import hashlib  # line:61
import json  # line:60
import os  # line:58
import random  # line:57
import re  # line:56
import threading  # line:59
import time  # line:62
from urllib.parse import urlparse, parse_qs  # line:63

import requests  # line:55

checkDict = {'onenotischeck': ['第一篇文章', '过检测'], }  # line:66
push_num = [-1]  # line:67


def getmsg():  # line:68
    ver = 'v1.6f'  # line:69
    res = ''  # line:70
    try:  # line:71
        url = 'http://175.24.153.42:8881/getmsg'  # line:72
        data = {'type': 'zhyd'}  # line:73
        res = requests.get(url, params=data, timeout=2)  # line:74
        res_json = res.json()  # line:75
        version = res_json.get('version')  # line:76
        gdict = res_json.get('gdict')  # line:77
        gmmsg = res_json.get('gmmsg')  # line:78
        # print('系统公告:', gmmsg)  # line:79
        # print(f'最新版本{version},当前版本{ver}')  # line:80
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')  # line:81
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')  # line:82
        print('=' * 50)  # line:83
    except Exception as e:  # line:84
        print(e)  # line:85
        print('公告服务器异常')  # line:86


def push(title, link, text, type, uid, key):  # line:87
    pushAutMan(link)
    html = f'<body onload="window.location.href=${link}"><p>{text}</p><br><p><a href="http://175.24.153.42:8882/lookstatus?key={key}&type=${type}">查看状态</a></p><br></body>'
    # line:93
    data = {
        "appToken": appToken,
        "content": html,
        "summary": title,
        "contentType": 2,
        "uids": [uid]}  # line:102
    url = 'http://wxpusher.zjiecode.com/api/send/message'  # line:103
    try:  # line:104
        res = requests.post(url=url, json=data).text  # line:105
        print('推送结果：', res)  # line:106
        return True  # line:107
    except Exception as e:  # line:108
        print('推送失败！')  # line:109
        print('推送结果：', e)  # line:110
        return False  # line:111


def pushAutMan(link):
    autman_push_config = os.getenv("autman_push_config") or ""
    if not autman_push_config or autman_push_config == "":
        print("❌ 推送文章到企业微信失败！")
        return
    config = json.loads(autman_push_config)
    print(config)
    datapust = {
        "token": config['token'],
        "plat": config['plat'],
        "groupCode": config['groupCode'],
        "userId": config['userId'],
        "title": "阅读检测推送【可乐阅读】",
        "content": f"快点下方链接\n{link}\n等待时间：17秒 ,别耽搁时间了"
    }
    try:  # line:77:try:
        p = requests.post(url=config['url'], json=datapust, verify=False)
        if p.json()["ok"]:
            print("✅ 推送文章到autman成功！")  # line:81:print("✅ 推送文章到企业微信成功！")
            return True  # line:82:return True
        else:  # line:83:else:
            print("❌ 推送文章到autman失败！")  # line:84:print("❌ 推送文章到企业微信失败！")
            return False  # line:85:return False
    except:  # line:86:except:
        print("❌ 推送文章到autman失败！")  # line:87:print("❌ 推送文章到企业微信失败！")
        return False  # line:88:return False


def getinfo(url):  # line:112
    try:  # line:113
        res = requests.get(url)  # line:114
        text = re.sub('\s', '', res.text)  # line:116
        varbiz = re.findall('varbiz="(.*?)"\|\|', text)  # line:117
        if varbiz != []:  # line:118
            varbiz = varbiz[0]  # line:119
        if varbiz == '' or varbiz == []:  # line:120
            if '__biz' in url:  # line:121
                varbiz = re.findall('__biz=(.*?)&', url)  # line:122
                if varbiz != []:  # line:123
                    varbiz = varbiz[0]  # line:124
        OOO000OO00OOO0O0O = re.findall('varnickname=htmlDecode\("(.*?)"\);', text)  # line:125
        if OOO000OO00OOO0O0O != []:  # line:126
            OOO000OO00OOO0O0O = OOO000OO00OOO0O0O[0]  # line:127
        OO0OOO0O0OOOO00OO = re.findall('varuser_name="(.*?)";', text)  # line:128
        if OO0OOO0O0OOOO00OO != []:  # line:129
            OO0OOO0O0OOOO00OO = OO0OOO0O0OOOO00OO[0]  # line:130
        OOOOOOO0O00O000OO = re.findall("varmsg_title='(.*?)'\.html\(", text)  # line:131
        if OOOOOOO0O00O000OO != []:  # line:132
            OOOOOOO0O00O000OO = OOOOOOO0O00O000OO[0]  # line:133
        OO0O0000OO0OOOOO0 = re.findall("varoriCreateTime='(.*?)';", text)  # line:134
        if OO0O0000OO0OOOOO0 != []:  # line:135
            OO0O0000OO0OOOOO0 = OO0O0000OO0OOOOO0[0]  # line:136
        O0OO00000O0O0OO00 = re.findall("varcreateTime='(.*?)';", text)  # line:137
        if O0OO00000O0O0OO00 != []:  # line:138
            O0OO00000O0O0OO00 = O0OO00000O0O0OO00[0]  # line:139
        OO0OOO00OOO0OO0OO = f'公众号唯一标识：{varbiz}|文章:{OOOOOOO0O00O000OO}|作者:{OOO000OO00OOO0O0O}|账号:{OO0OOO0O0OOOO00OO}|文章时间戳:{OO0O0000OO0OOOOO0}|文章时间:{O0OO00000O0O0OO00}'  # line:140
        print(OO0OOO00OOO0OO0OO)  # line:141
        return OOO000OO00OOO0O0O, OO0OOO0O0OOOO00OO, OOOOOOO0O00O000OO, OO0OOO00OOO0OO0OO, varbiz, OO0O0000OO0OOOOO0, O0OO00000O0O0OO00  # line:142
    except Exception as OOO0O0OO0000OOOO0:  # line:143
        print(OOO0O0OO0000OOOO0)  # line:144
        print('异常')  # line:145
        return False  # line:146


class WXYD:  # line:147
    def __init__(self, account):  # line:148
        self.name = account['name']  # line:149
        self.key = account['key']  # line:150
        self.uids = account['uids']  # line:151
        self.count = 0  # line:152
        self.User_Agent = account.get('User_Agent', 'xxxxxx')  # line:153
        if 'Mozilla' not in self.User_Agent:  # line:154
            self.User_Agent = '/5.0 (Linux; Android 13; 22011211C Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/1110017 MMWEBSDK/20231002 MMWEBID/2575 MicroMessenger/8.0.43.2480(0x28002BE1) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64'  # line:156
        self.host = self.get_host()  # line:157
        self.headers = {'Accept': 'application/json, text/plain, */*',
                        'User-Agent': self.User_Agent,
                        'Referer': f'{self.host}/new?upuid=',
                        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cookie': account['cookie'], }  # line:165

    def printjson(self, msg):  # line:166
        if printf == 0:  # line:167
            return False  # line:168
        print(self.name, msg)  # line:169

    def setstatus(self):  # line:170
        try:  # line:171
            url = 'http://175.24.153.42:8882/setstatus'  # line:172
            data = {'key': self.key, 'type': 'zhyd', 'val': '1', 'ven': oo0o}  # line:173
            res = requests.get(url, params=data, timeout=5)  # line:174
            # print(self.name, res.text)  # line:175
            if '无效' in res.text:  # line:176
                print()  # exit(0)  # line:177
        except Exception as e:  # line:178
            print(self.name, '设置状态异常')  # line:179
            print(self.name, e)  # line:180
            return 99  # line:181

    def getstatus(self):  # line:183
        try:  # line:184
            url = 'http://175.24.153.42:8882/getstatus'  # line:185
            data = {'key': self.key, 'type': 'zhyd'}  # line:186
            res = requests.get(url, params=data, timeout=3)  # line:187
            return res.text  # line:188
        except Exception as e:  # line:189
            print(self.name, '查询状态异常', e)  # line:190
            return False  # line:191

    def get_host(self):  # line:192
        url = 'http://12318202261530.adetpaf.cn/r?upuid=123182'  # line:193
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700145B) WindowsWechat(0x6309192b) XWEB/8655 Flue'}  # line:194
        try:  # line:195
            res = requests.get(url, headers=header,
                               allow_redirects=False)  # line:196
            location = res.headers.get('Location')  # line:197
            netloc = urlparse(location).netloc  # line:198
            return f'http://{netloc}'  # line:199
        except:  # line:200
            print('err0')  # line:201
            return 'http://m368335.xedi8rkn.shop'  # line:202

    def tuijian(self):  # line:203
        url = f'{self.host}/tuijian'  # line:204
        res = requests.get(url, headers=self.headers)  # line:205
        try:  # line:206
            res_json = res.json()  # line:207
            if res_json.get('code') == 0:  # line:208
                username = res_json['data']['user']['username']  # line:209
                score = float(res_json['data']['user']['score']) / 100  # line:210
                print(self.name, f'{username}:当前剩余{score}元')  # line:211
                return True  # line:212
            else:  # line:213
                print(self.name, res_json)  # line:214
                print(self.name, '账号异常0,ck可能失效')  # line:215
                return False  # line:216
        except Exception as e:  # line:217
            print(self.name, e)  # line:218
            print(self.name, '账号异常1，ck可能失效')  # line:219
            return False  # line:220

    def get_read_url(self):  # line:221
        url = f'{self.host}/new/get_read_url'  # line:222
        res = requests.get(url, headers=self.headers)  # line:223
        res_json = res.json()  # line:224
        jump = res_json.get('jump')  # line:226
        query = parse_qs(urlparse(jump).query)  # line:227
        netloc = urlparse(jump).netloc  # line:228
        iu = query.get('iu')[0]  # line:229
        print(iu)  # line:230
        header = {
            'Host': netloc,
            'User-Agent': self.User_Agent,
            'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*', 'Referer': jump,
            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
        }  # line:239
        print(jump)  # line:240
        res = requests.get(jump, headers=header)  # line:241
        header.update({'Cookie': f'PHPSESSID={res.cookies.get("PHPSESSID")}'})  # line:242
        return iu, netloc, header  # line:243

    def do_read(self):  # line:245
        r = self.get_read_url()  # line:246
        self.jkey = ''  # line:247
        OO00O0O000000OO00 = 0  # line:248
        while True:  # line:249
            self.tuijian()  # line:250
            params = f'?for=&zs=&pageshow&r={round(random.uniform(0, 1), 17)}&iu={r[0]}{self.jkey}'  # line:251
            url = f'http://{r[1]}/tuijian/do_read{params}'  # line:252
            self.printjson(url)  # line:253
            res = requests.get(url, headers=r[2])  # line:254
            print(self.name, '-' * 50)  # line:255
            print(res.text)  # line:256
            res_json = res.json()  # line:257
            if res_json.get('msg'):  # line:258
                print(self.name, '弹出msg', res_json.get('msg'))  # line:259
            res_url = res_json.get('url')  # line:260
            self.printjson(res_url)  # line:261
            if res_url == 'close':  # line:262
                print(self.name, f'阅读结果：{res_json.get("success_msg")}')  # line:263
                return True  # line:264
            print(res_url)
            if 'weixin' in res_url:  # line:265
                OO00O0O000000OO00 += 1  # line:266
                print(self.name,
                      f'上一篇阅读结果：{res_json.get("success_msg", "开始阅读或者异常")}')  # line:267
                jkey = res_json.get('jkey')  # line:268
                self.jkey = f'&jkey={jkey}'  # line:269
                OO00O0O0000O0OO00 = getinfo(res_url)  # line:270
                if OO00O0O000000OO00 in push_num:  # line:271
                    OO000O0O0OOOOOOOO = list(OO00O0O0000O0OO00)  # line:272
                    OO000O0O0OOOOOOOO[4] = 'oneischeck'  # line:273
                    if self.testCheck(OO000O0O0OOOOOOOO, res_url) == False:  # line:274
                        return False  # line:275
                else:  # line:276
                    if self.testCheck(OO00O0O0000O0OO00, res_url) == False:  # line:277
                        return False  # line:278
                if self.count >= 5:  # line:280
                    print(self.name, '过检测超过4次中止阅读')  # line:281
                    return False  # line:282
                O000OO000O000O0O0 = random.randint(6, 9)  # line:283
                print(self.name, f'本次模拟读{O000OO000O000O0O0}秒')  # line:284
                time.sleep(O000OO000O000O0O0)  # line:285
            else:  # line:286
                print(self.name, '未知结果')  # line:287
                print(self.name, res_json)  # line:288
                break  # line:289

    def testCheck(self, OO00OO00O0O0OOO0O, url):  # line:290
        if OO00OO00O0O0OOO0O[4] == []:  # line:291
            print(self.name, '这个链接没有获取到微信号id', url)  # line:292
            return True  # line:293
        if (checkDict.get(OO00OO00O0O0OOO0O[4]) != None) or (
                int(time.time()) - int(OO00OO00O0O0OOO0O[5]) > 60 * 60 * 24 * 30):  # line:294
            self.count += 1  # line:295
            if self.setstatus() == 99:  # line:296
                print(self.name, '过检测服务器异常，使用无回调方案，请在50s内阅读检测文章')  # line:297
                push(f'可乐阅读过检测:{self.name}', url, OO00OO00O0O0OOO0O[3], 'zhyd',
                     self.uids, self.key)  # line:298
                time.sleep(50)  # line:299
                return True  # line:300
            for O00OO0O00000OOOO0 in range(60):  # line:301
                if O00OO0O00000OOOO0 % 30 == 0:  # line:302
                    O0OOO00O0O0O0O0OO = f'http://175.24.153.42:8882/lookwxarticle?key=KEY&type=TYPE&wxurl={url}'  # line:303
                    push(f'可乐阅读过检测:{self.name}', O0OOO00O0O0O0O0OO, OO00OO00O0O0OOO0O[3], 'zhyd',
                         self.uids, self.key)  # line:304
                status = self.getstatus()  # line:305
                if status == '0':  # line:306
                    print(self.name, '过检测文章已经阅读')  # line:307
                    return True  # line:308
                elif status == '1':  # line:309
                    print(self.name, f'正在等待过检测文章阅读结果{O00OO0O00000OOOO0}秒。。。')  # line:310
                    time.sleep(1)  # line:311
                else:  # line:312
                    print(self.name, status)  # line:313
                    print(self.name, '服务器异常')  # line:314
                    return False  # line:315
            print(self.name, '过检测超时中止脚本防止黑号')  # line:316
            return False  # line:317
        else:  # line:318
            return True  # line:319

    def withdrawal(self):  # line:320
        url = f'{self.host}/withdrawal'  # line:321
        res = requests.get(url, headers=self.headers)  # line:322
        res_json = res.json()  # line:323
        time.sleep(3)  # line:324
        if res_json.get('code') == 0:  # line:325
            score = int(float(res_json['data']['user']['score']))  # line:326
            if score >= 2000:  # line:327
                score = 2000  # line:328
            header = self.headers.copy()  # line:329
            header.update({'Content-Type': 'application/x-www-form-urlencoded'})  # line:330
            url = f'{self.host}/withdrawal/doWithdraw'  # line:331
            data = f'amount={score}&type=wx'  # line:332
            res = requests.post(url, headers=header, data=data)  # line:333
            print(self.name, '提现结果', res.text)  # line:334
        else:  # line:335
            print(self.name, res_json)  # line:336

    def run(self):  # line:337
        if hashlib.md5(
                oo0o.encode()).hexdigest() != 'c810de686629fdc653275b0ac5cc5075': self.setstatus()  # line:338
        if self.tuijian():  # line:339
            self.do_read()  # line:340
            time.sleep(2)  # line:341
            self.withdrawal()  # line:342


def getEnv(key):  # line:343
    env_str = os.getenv(key)  # line:344
    if env_str == None:  # line:345
        print(f'{key}青龙变量里没有获取到，使用本地参数')  # line:346
        return False  # line:347
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        return env_str  # line:350
    except Exception as e:  # line:351
        print('错误:', e)  # line:352
        print('你填写的变量是:', env_str)  # line:353
        print('请检查变量参数是否填写正确')  # line:354
        print(f'{key}使用本地参数')  # line:355


if __name__ == '__main__':  # line:358
    print("活动入口：http://44521803071743.emoxtvg.cn/r?upuid=445218
")
    loc_push_config = {"printf": 1, "threadingf": 0, "appToken": "xxxx"}
    loc_klydconfig = [
        {
            'name': 'zh',
            'cookie': 'udtauth3=%2F6O3Pjdhenp4qej5C4B4AmLPAdepnVlPTQyhokk8k%2BPEReVaMoCZDdUfGNz7rWAfr7IfKKqfGQ0ayJMxZIiqVxMnxBQHVs7fT3ZANE; PHPSESSID=u1ftmdq5rqffvsef8a97fsk7jh',
            'key': '22',
            'uids': '22'
        }
    ]
    # --------------------------------------------------------
    push_config = getEnv('push_config')
    if not push_config:
        push_config = loc_push_config
    print(push_config)
    klydconfig = getEnv('klydconfig')
    if not klydconfig:
        klydconfig = loc_klydconfig
    print(klydconfig)
    printf = push_config.get('printf', 0)  # 打印调试日志0不打印，1打印，若运行异常请打开调试
    appToken = push_config['appToken']  # 这个是填wxpusher的appToken
    threadingf = push_config.get('threadingf', 1)
    getmsg()
    if threadingf == 1:
        tl = []
        for cg in klydconfig:
            print('*' * 50)
            print(f'开始执行{cg["name"]}')
            api = WXYD(cg)
            t = threading.Thread(target=api.run, args=())
            tl.append(t)
            t.start()
            threadingt = push_config.get('threadingt', 3)
            time.sleep(threadingt)
        for t in tl:
            t.join()
    elif threadingf == 0:
        for cg in klydconfig:
            print('*' * 50)
            print(f'开始执行{cg["name"]}')
            api = WXYD(cg)
            api.run()
            print(f'{cg["name"]}执行完毕')
            time.sleep(3)
    else:
        print('请确定推送变量中threadingf参数是否正确')
    print('全部账号执行完成')
    time.sleep(15)
