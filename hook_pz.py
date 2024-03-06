"""
仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
2024-01-12 14:30:38
# 反馈群：https://t.me/vhook_wool

抓包教程：无需抓包，填写手机号密码即可
export pzzh=手机号#密码@手机号#密码
cron：0 0 7 * * ?
"""
import base64
import os
import random

import requests
import notify


def utf16_to_utf8(s):
    utf8_chars = []
    for char in s:
        code_point = ord(char)
        if 0 < code_point <= 127:
            utf8_chars.append(char)
        elif 128 <= code_point <= 2047:
            utf8_chars.append(chr(192 | code_point >> 6 & 31))
            utf8_chars.append(chr(128 | 63 & code_point))
        elif 2048 <= code_point <= 65535:
            utf8_chars.append(chr(224 | code_point >> 12 & 15))
            utf8_chars.append(chr(128 | code_point >> 6 & 63))
            utf8_chars.append(chr(128 | 63 & code_point))
    return ''.join(utf8_chars)


def encode(s):
    if not s:
        return ""

    utf8_str = utf16_to_utf8(s)
    base64_encoded = base64.b64encode(utf8_str.encode()).decode()

    return base64_encoded


def jiami(mw):
    encoded_str = encode(mw)

    random_values = [random.choice("0123456789ABCDEF") for _ in range(400)]

    result = (
            ''.join(random_values[:100]) +
            encoded_str[:8] +
            ''.join(random_values[100:200]) +
            encoded_str[8:20] +
            ''.join(random_values[200:300]) +
            encoded_str[20:] +
            ''.join(random_values[300:])
    )

    return result


def login(zh, mm):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Authorization': 'Bearer',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://xip.ipzan.com',
        'Pragma': 'no-cache',
        'Referer': 'https://xip.ipzan.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    str = f"{zh}QWERIPZAN1290QWER{mm}"
    mw = jiami(str)
    json_data = {"account": mw, "source": "ipzan-home-one"}
    response = requests.post('https://service.ipzan.com/users-login', headers=headers, json=json_data)
    if response.json()["code"] == 0:
        print("登录成功")
        token = response.json()["data"]
        qd(token)
        # print(token)
    else:
        print("登录失败")


def qd(token):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Authorization": f"Bearer {token}",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://xip.ipzan.com",
        "Pragma": "no-cache",
        "Referer": "https://xip.ipzan.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    }
    url = "https://service.ipzan.com/home/userWallet-receive"
    response = requests.get(url, headers=headers)
    print(response.text)


def get_env(key):
    if os.environ.get(key) is None:
        print(f"未填写环境变量{key}")
        return os.environ.get(key)
    else:
        return os.environ.get(key)


if __name__ == '__main__':
    env_str = get_env("pzzh")
    if not env_str:
        print("未填写环境变量:export pzzh=手机号#密码@手机号#密码")
        exit()
    users = env_str.split("&")
    print(f"检测到{len(users)}个账号")
    for user in users:
        arr = user.split("#")
        zh = arr[0]
        mm = arr[1]
        print(f"开始执行账号[{zh}]")
        login(zh, mm)
