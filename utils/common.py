#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests


def check_cloud(name, local_ver=1.0):
    res = requests.get("https://jihulab.com/vhook/control/-/raw/main/ql.json")
    if res.status_code == 200:
        verRes = res.json().get(name, {})
        if verRes:
            r_ver = verRes['ver']
            r_log = verRes['log']
            r_tip = verRes['tip']
            r_open = verRes['open']
            r_date = verRes['date']
            r_tg = verRes['tg']
            r_inviteUrl =  verRes['inviteUrl']
            if not r_open:
                content = r_tip
                content += f"【反馈群】：{r_tg}"
                exit(content)
            if local_ver < r_ver:
                content = "发现新版本:"
                content += f"\n【反馈群】：{r_tg}"
                content += f"\n【版本号】：V{r_ver}"
                content += f"\n【更新日期】：{r_date}"
                content += f"\n【更新内容】：{r_log}"
                if r_inviteUrl:
                    content += f"\n【项目入口】：{r_inviteUrl}"
                exit(content)

            content = f"\n【反馈群】：{r_tg}"
            content += f"\n【当前版本】：V{local_ver}"
            content += f"\n【更新日期】：{r_date}"
            content += f"\n【更新内容】：{r_log}"

            if r_inviteUrl:
                content += f"\n【项目入口】：{r_inviteUrl}"
            print(content)
