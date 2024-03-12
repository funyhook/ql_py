"""
软件:建行生活
# 反馈群：https://t.me/vhook_wool

仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
2024-01-12 14:30:38
活动信息: 奋斗季cc豆 功能：每日营收，签到 浏览任务，答题，抽奖，专区任务
先开抓包，先开抓包，进建行生活app，没抓到等两小时在抓
https://yunbusiness.ccb.com/basic_service/txCtrl?  请求头中token值，deviceid值。
请求体meb_id或者userid值
专区任务，专区抓fission-events.ccbft.com，全部cookie

export hook_ccb='[{
    "deviceid": "1212",
    "meb_id": "1212",
    "phone": "1212",
    "token": "1212",
    "cookie": "1212",
}]'
# cron：0 0 7 * * ?
# 注: 此脚本仅限个人使用,不得传播
"""
import json
import os
import random
import re
import time
from datetime import datetime
from urllib.parse import quote
from utils import common

import requests

user_cookie = [{
    "deviceid": "1212",
    "meb_id": "1212",
    "phone": "1212",
    "token": "1212",
    "cookie": "1212",
}]
'''
doll_flag  1开启抓娃娃，0关闭
doll_draw 抓娃娃次数，总数小于10
'''
doll_flag = 0  # 1开启抓娃娃，0关闭
doll_draw = 1

'''
basket_flag  1开启投篮球，0关闭
basket_draw  投篮球次数，总数小于5
'''
basket_flag = 1
basket_draw = 5

'''
box_flag   1开启开盲盒，0关闭
box_id  开盲盒类型，1为88豆，2为188豆，3为10000豆
box_draw   开盲盒次数，总数小于5
'''
box_flag = 0
box_id = 1
box_draw = 2

debug = 0


class CCD:
    base_header = {
        'Host': 'm3.dmsp.ccb.com',
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://m3.dmsp.ccb.com',
        'x-requested-with': 'com.tencent.mm',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json'
    }
    token_headers = {
        'Host': 'event.ccbft.com',
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://event.ccbft.com',
        'x-requested-with': 'com.ccb.longjiLife',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json'
    }

    def __init__(self, ccb_cookie):
        self.deviceid = ccb_cookie['deviceid']
        self.meb_id = ccb_cookie['meb_id']
        self.phone = ccb_cookie['phone']
        self.ccb_token = ccb_cookie['token']
        self.zq_cookie = ccb_cookie['cookie']
        self.ccbParam = None
        self.ccb_uuid = None
        self.zhc_token = None
        self.zq_headers = {
            'Host': 'fission-events.ccbft.com',
            'accept': 'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://fission-events.ccbft.com',
            'Cookie': self.zq_cookie,
            'content-type': 'application/json'
        }

    # 随机延迟默认1-1.5
    def sleep(self, min_delay=1, max_delay=1.5):
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def send_request(self, url, headers, data=None, method='GET', cookies=None):
        with requests.Session() as session:
            session.headers.update(headers)
            if cookies is not None:
                session.cookies.update(cookies)

            try:
                if method == 'GET':
                    response = session.get(url)
                elif method == 'POST':
                    response = session.post(url, json=data)
                else:
                    raise ValueError('Invalid HTTP method.')

                response.raise_for_status()
                if debug:
                    print(response.json())
                return response.json()

            except requests.Timeout as e:
                print("请求超时:", str(e))

            except requests.RequestException as e:
                print("请求错误:", str(e))

            except Exception as e:
                print("其他错误:", str(e))

            return None

    def encrypt(self, text):
        res = requests.post('http://82.157.10.108:8086/get_jhenc', data={'encdata': text})
        return res.text

    # 刷新session
    def auto_login(self):
        cookies = {
        }

        headers = {
            'Host': 'yunbusiness.ccb.com',
            'user-agent': '%E5%BB%BA%E8%A1%8C%E7%94%9F%E6%B4%BB/2023031502 CFNetwork/1404.0.5 Darwin/22.3.0',
            'devicetype': 'iOS',
            'mbc-user-agent': f'MBCLOUDCCB/iPhone/iOS16.3.1/2.15/2.1.5/7E1BDB39-5CF8-4B88-BB12-AFF439B6A249/chinamworld/750*1334/2.1.5.002/1.0/{self.deviceid}/iPhone8Global/iOS/iOS16.3.1',
            'appversion': '2.1.5.002',
            'ua': 'IPHONE',
            'clientallver': '2.1.5.002',
            'deviceid': self.deviceid,
            'accept-language': 'zh-CN,zh-Hans;q=0.9',
            'c-app-id': '03_64e1367661ee4091acc04ce98f3660e6',
            'accept': 'application/json',
            'content-type': 'application/json',
        }

        params = {
            'txcode': 'autoLogin',
        }

        data = {
            "Token": self.ccb_token}
        data = json.dumps(data)
        data = quote(self.encrypt(data))
        response = requests.post('https://yunbusiness.ccb.com/clp_service/txCtrl', params=params,
                                 cookies=cookies,
                                 headers=headers, data=data)

        setCookie = response.headers.get('Set-Cookie')
        if setCookie:
            session_cookie = re.search(r'SESSION=([^;]+)', setCookie)
            session_value = session_cookie.group(1)

            param_url = 'https://yunbusiness.ccb.com/basic_service/txCtrl?txcode=A3341SB06'
            param_payload = {
                "regionCode": "110000",
                "PLATFORM_ID": "YS44000010000078",
                "chnlType": "1",
                "APPEND_PARAM": "",
                "ENCRYPT_MSG": f"BGCOLOR=&userid={self.meb_id}&mobile={self.phone}&orderid=&PLATFLOWNO=1051000101693904952945620&cityid=610100&openid=&Usr_Name=&USERID={self.meb_id}&MOBILE={self.phone}&ORDERID=&CITYID=610100&OPENID=&userCityId=360400&lgt=116.25548583307314&ltt=29.36255293895674&USERCITYID=360400&LGT=116.25548583307314&LTT=29.36255293895674&GPS_TYPE=gcj02&MOBILE={self.phone}&CrdtType=1010&CrdtNo=231212"
            }

            headers['cookie'] = f'SESSION={session_value}'
            param_data = requests.post(param_url, headers=headers, json=param_payload).json()
            errCode = param_data.get('errCode')
            if errCode != '0':
                print(param_data)
            else:
                self.ccbParam = param_data.get('data', {}).get('ENCRYPTED_MSG', '')
                self.get_token()
            return session_value
        else:
            print(f'session刷新失败，{response.text}')

    def get_token(self):
        try:
            url = f"https://event.ccbft.com/api/flow/nf/shortLink/redirect/ccb_gjb?CCB_Chnl=2030023&ccbParamSJ={self.ccbParam}&cityid=110000&CITYID=110000&userCityId=110000&USERCITYID=110000"

            payload = {
                "shortId": "polFsWD2jPnjhOx9ruVBcA",
                "archId": "ccb_gjb",
                "ccbParamSJ": self.ccbParam,
                "channelId": "ccbLife",
                "ifCcbLifeFirst": True
            }

            return_data = self.send_request(url, headers=self.token_headers, data=payload, method='POST')

            redirect_url = return_data['data'].get('redirectUrl')
            self.ccb_uuid = return_data['data'].get('ccbLifeUUID')
            token = self.extract_token(redirect_url)
            if token:
                self.zhc_token = token
                if self.auth_login(token):
                    self.user_info()
                    self.sign_in()
                    self.getlist()
                    self.answer_state()
                    print('\n======== 专区任务 ========')
                    time.sleep(random.randint(3, 5))
                    self.get_csrftoken()
                    self.get_user_ccd()
                else:
                    print(return_data)
        except Exception as e:
            print(f"get_token err {e.with_traceback()}")

    def extract_token(self, redirect_url):
        start_token_index = redirect_url.find("__dmsp_token=") + len("__dmsp_token=")
        end_token_index = redirect_url.find("&", start_token_index)

        token = None
        if start_token_index != -1 and end_token_index != -1:
            token = redirect_url[start_token_index:end_token_index]
        return token

    # 登录
    def auth_login(self, token):
        url = 'https://m3.dmsp.ccb.com/api/businessCenter/auth/login'
        payload = {"token": token, "channelId": "ccbLife"}
        return_data = self.send_request(url, headers=self.base_header, data=payload, method='POST')
        self.sleep()
        if return_data['code'] != 200:
            print(return_data['message'])
            return False
        else:
            return True

    # 查询用户等级
    def user_info(self):
        url = f'https://m3.dmsp.ccb.com/api/businessCenter/mainVenue/getUserState?zhc_token={self.zhc_token}'
        return_data = self.send_request(url, headers=self.base_header, method='POST')
        if return_data['code'] != 200:
            print(return_data['message'])
        else:
            current_level = return_data['data'].get('currentLevel')
            need_exp = return_data['data'].get('nextMonthProtectLevelNeedGrowthExp') - return_data['data'].get(
                'growthExp')
            level = return_data['data'].get('currentProtectLevel')
            if return_data['data'].get('zhcRewardInfo'):
                reward_id = return_data['data'].get('zhcRewardInfo').get('id')
                reward_type = return_data['data'].get('zhcRewardInfo').get('rewardType')
                reward_value = return_data['data'].get('zhcRewardInfo').get('rewardValue')
                print(f"当前用户等级{current_level}级")
                print(f"距下一级还需{need_exp}成长值")
                self.income(level, reward_id, reward_type, reward_value)
            else:
                print("查询收入明细出现错误！")

    # 每日营收
    def income(self, level, reward_id, reward_type, reward_value):
        url = f'https://m3.dmsp.ccb.com/api/businessCenter/mainVenue/receiveLevelReward?zhc_token={self.zhc_token}'
        payload = {"level": level, "rewardId": reward_id, "levelRewardType": reward_type}
        return_data = self.send_request(url, headers=self.base_header, data=payload, method='POST')
        self.sleep()
        if return_data['code'] != 200:
            print(return_data['message'])
        else:
            print(f"今日营收: {reward_value}cc豆")

    # 每日勋章

    # 签到
    def sign_in(self):
        signin_url = f'https://m3.dmsp.ccb.com/api/businessCenter/taskCenter/signin?zhc_token={self.zhc_token}'
        signin_payload = {"taskId": 96}
        return_data = self.send_request(url=signin_url, headers=self.base_header, data=signin_payload,
                                        method='POST')
        self.sleep()
        if return_data['code'] != 200:
            print(return_data['message'])
        else:
            print(return_data['message'])

    # 获取浏览任务列表
    def getlist(self):
        try:
            list_url = f'https://m3.dmsp.ccb.com/api/businessCenter/taskCenter/getTaskList?zhc_token={self.zhc_token}'
            payload = {"publishChannels": "03", "regionId": "110100"}  # 440300

            return_data = self.send_request(url=list_url, headers=self.base_header, data=payload, method='POST')

            if return_data['code'] != 200:
                print(return_data['message'])
            else:
                task_list = return_data['data'].get('浏览任务')

                for value in task_list:
                    complete_status = value['taskDetail'].get('completeStatus')

                    if complete_status == '02':
                        print(f"--已完成: {value['taskName']}")
                    else:
                        task_id = value['id']
                        task_name = value['taskName']
                        print(f'---去完成: {task_name}')
                        self.execute_task(task_id)
        except Exception as e:
            print(e)

    def execute_task(self, task_id):
        try:
            browse_url = f'https://m3.dmsp.ccb.com/api/businessCenter/taskCenter/browseTask?zhc_token={self.zhc_token}'
            receive_url = f'https://m3.dmsp.ccb.com/api/businessCenter/taskCenter/receiveReward?zhc_token={self.zhc_token}'
            payload = {"taskId": task_id, "browseSec": 1}

            browse_data = self.send_request(browse_url, headers=self.base_header, data=payload, method='POST')

            if browse_data['code'] != 200:
                print(browse_data['message'])
            else:
                print(browse_data['message'])

                receive_data = self.send_request(receive_url, headers=self.base_header, data=payload,
                                                 method='POST')
                if receive_data['code'] != 200:
                    print(receive_data['message'])
                else:
                    print(receive_data['message'])
        except Exception as e:
            print(e)

    # 获取答题state
    def answer_state(self):
        url = f'https://m3.dmsp.ccb.com/api/businessCenter/zhcUserDayAnswer/getAnswerStatus?zhc_token={self.zhc_token}'
        return_data = self.send_request(url, headers=self.base_header)
        if return_data['code'] == 200:
            if return_data['data'].get('answerState') == 'Y':
                print(return_data['message'])
            else:
                # 获取今日题目
                print('获取今日题目')
                self.get_question()
        else:
            print(return_data['message'])

    # 获取题目
    def get_question(self):
        url = f'https://m3.dmsp.ccb.com/api/businessCenter/zhcUserDayAnswer/queryQuestionToday?zhc_token={self.zhc_token}'
        return_data = self.send_request(url, headers=self.base_header)
        self.sleep()
        if return_data['code'] != 200:
            print(return_data['message'])
        else:
            question_id = return_data['data'].get('questionId')
            remark = return_data['data'].get('remark')
            answer_list = return_data['data'].get('answerList')
            if remark:
                # 匹配答案
                print('开始匹配正确答案')
                pattern = r"[，。？！“”、]"
                remark_cleaned = re.sub(pattern, "", remark)

                max_match_count = 0
                right_answer_id = None
                for answer in answer_list:
                    answer_id = answer["id"]
                    answer_result = answer["answerResult"]
                    answer_cleaned = re.sub(pattern, "", answer_result)

                    match_count = 0
                    for word in answer_cleaned:
                        if word in remark_cleaned:
                            match_count += 1
                            remark_cleaned = remark_cleaned.replace(word, "", 1)

                    if match_count > max_match_count:
                        max_match_count = match_count
                        right_answer_id = answer_id
                if right_answer_id is not None:
                    print("匹配成功，开始答题")
                else:
                    print("匹配失败，随机答题")
                    right_answer_id = random.choice(answer_list)['id']
                self.answer(question_id, right_answer_id)
            else:
                print('暂无提示随机答题')
                right_answer_id = random.choice(answer_list)['id']
                self.answer(question_id, right_answer_id)

    # 答题
    def answer(self, question_id, answer_ids):
        url = f'https://m3.dmsp.ccb.com/api/businessCenter/zhcUserDayAnswer/userAnswerQuestion?zhc_token={self.zhc_token}'
        payload = {"questionId": question_id, "answerIds": answer_ids}
        return_data = self.send_request(url, headers=self.base_header, data=payload, method='POST')
        self.sleep()
        if return_data['code'] != 200:
            print(return_data['message'])
        else:
            print(return_data['message'])

    # ---------下面是精彩专区任务--------
    def get_csrftoken(self):
        refresh_url = 'https://event.ccbft.com/api/flow/nf/shortLink/redirect/ccb_gjb?CCB_Chnl=6000117'
        payload = '{{"shortId":"m13hviAVn3cy3PFWPRBB_w","archId":"ccb_gjb","ccbParamSJ":null,"channelId":"ccbLife","ifCcbLifeFirst":false,"ccbLifeUUID":"{}"}}'.format(
            self.ccb_uuid)

        headers = {
            'Host': 'fission-events.ccbft.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'x-requested-with': 'com.ccb.longjiLife',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'referer': 'https://event.ccbft.com/',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': self.zq_cookie
        }

        return_data = requests.post(refresh_url, headers=self.token_headers, data=payload).json()
        print(return_data)
        if return_data['code'] != 200:
            print(return_data['message'])

        else:
            redirect_url = return_data['data'].get('redirectUrl')
            requests.get(url=redirect_url, headers=headers)
            # 使用正则__dmsp_st的值
            match = re.search(r'__dmsp_st=([^&]+)', redirect_url)

            if match:
                dmsp_st_value = match.group(1)
                try:
                    url2 = f'https://fission-events.ccbft.com/a/224/1m0xM2mx?CCB_Chnl=6000117&__dmsp_st={dmsp_st_value}'
                    res = requests.get(url=url2, headers=headers)
                    print(res.text)
                    data = res.text
                    csrf_token, authorization = self.extract_csrf_and_auth(data)

                    if csrf_token and authorization:
                        self.zq_headers['x-csrf-token'] = csrf_token
                        self.zq_headers['authorization'] = f'Bearer {authorization}'
                        self.sleep()

                        print('\n----代发专区----')
                        # self.game_id()
                        print('\n----养老专区----')
                        self.turn()
                        print('\n----跨境专区----')
                        self.border_draw()
                        print('\n----商户专区----')
                        self.shoplist()
                        print('\n----消保专区----\n---登山游戏----')
                        self.fire()
                        print('\n---抓娃娃游戏----')
                        self.get_doll()
                        print('\n---投篮球游戏----')
                        self.do_basket()
                        print('\n---开盲盒----')
                        self.open_box()
                    else:
                        print('CSRF token or Authorization not found.')
                except requests.RequestException as e:
                    print(f"请求异常: {e}")

    def extract_csrf_and_auth(self, data):
        csrf_token_pattern = r'<meta\s+name=csrf-token\s+content="([^"]+)">'
        authorization_pattern = r'<meta\s+name=Authorization\s+content="([^"]+)">'
        csrf_token_match = re.search(csrf_token_pattern, data)
        authorization_match = re.search(authorization_pattern, data)
        if csrf_token_match and authorization_match:
            return csrf_token_match.group(1), authorization_match.group(1)

        return None, None

    # 养老专区新
    def turn(self):
        tasklist_url = 'https://fission-events.ccbft.com/activity/dmspmileage/getindexdata/224/5P87Md3y'
        go_url = 'https://fission-events.ccbft.com/activity/dmspmileage/go/224/5P87Md3y'

        tasks_data = self.send_request(tasklist_url, headers=self.zq_headers)

        if not tasks_data or tasks_data['status'] != 'success':
            print(tasks_data['message'])
        else:
            task_list = tasks_data.get('data', {}).get('acttask', {}).get('limit_time')
            user_map_ident = tasks_data.get('data', {}).get('user_map_ident', '')

            print(f'当前是第 {user_map_ident} 张地图')

            rewards = tasks_data.get('data', {}).get('map', {}).get('config', {}).get('node')
            self.process_rewards(rewards)

            self.process_tasks(task_list)

            self.sleep()

            query_data = self.send_request(tasklist_url, headers=self.zq_headers)

            surplus = query_data.get('data', {}).get('mileage', {}).get('surplus')
            if surplus != '0':
                go_data = self.send_request(go_url, headers=self.zq_headers, method='POST')
                if go_data:
                    mileage_go = go_data.get('data', {}).get('mileage_go', '')
                    user_node = go_data.get('data', {}).get('user_node_value')
                    print(f'前进: {mileage_go}里程， 当前: {user_node}里程')
                    query_data2 = self.send_request(tasklist_url, headers=self.zq_headers)
                    rewards = query_data2.get('data', {}).get('map', {}).get('config', {}).get('node')
                    self.process_rewards(rewards)

    def process_rewards(self, rewards):
        for reward in rewards:
            value = reward.get('value')
            state = reward.get('state')
            if value == 0 or state != 3:
                continue
            elif value == 5000 and state == 4:
                replace_url = 'https://fission-events.ccbft.com/activity/dmspmileage/togglesmap/224/5P87Md3y'
                replace_data = self.send_request(replace_url, headers=self.zq_headers, method='POST')
                if replace_data and replace_data['status'] == 'success':
                    print('更换地图成功')
                    self.sleep()
            else:
                getreward_url = 'https://fission-events.ccbft.com/activity/dmspmileage/draw/224/5P87Md3y'
                reward_payload = {"value": value}
                rewrd_data = self.send_request(getreward_url, headers=self.zq_headers, data=reward_payload,
                                               method='POST')
                if rewrd_data['status'] != 'success':
                    return print(rewrd_data['message'])
                prizename = rewrd_data.get('data', {}).get('prizename')
                print(f'领取 {value}里程奖励: {prizename}')
                if value == 5000:
                    replace_url = 'https://fission-events.ccbft.com/activity/dmspmileage/togglesmap/224/5P87Md3y'
                    replace_data = self.send_request(replace_url, headers=self.zq_headers, method='POST')
                    if replace_data and replace_data['status'] == 'success':
                        print('更换地图成功')
                        self.sleep()
                time.sleep(3)

    def process_tasks(self, task_list):
        for task in task_list:
            ident = task.get('ident')
            title = task.get('title')
            state = task.get('state')
            reward = task.get('reward')
            if state == 1:
                print(f'--已完成: {title}')
            else:
                print(f'---去完成: {title}')
                dotask_url = 'https://fission-events.ccbft.com/activity/dmspmileage/taskgo/224/5P87Md3y'
                do_payload = {"type": "limit_time", "ident": ident}
                do_data = self.send_request(dotask_url, headers=self.zq_headers, data=do_payload, method='POST')
                if do_data and do_data['status'] == 'success':
                    print(f'--浏览成功获得: {reward} 里程')
                time.sleep(3)

    # 跨境专区新
    def border_draw(self):
        query_url = 'https://fission-events.ccbft.com/Component/draw/getUserExtInfo/224/1m0xM2mx'
        draw_url = 'https://fission-events.ccbft.com/Component/draw/commonDrawPrize/224/1m0xM2mx'

        query_data = self.send_request(query_url, headers=self.zq_headers)
        if query_data['status'] != 'success':
            print(query_data['message'])
        else:
            remain = query_data['data'].get('remain_num')
            if remain == '0':
                return print('--当前剩余抽奖次数为0')
            self.sleep()
            draw_data = self.send_request(draw_url, headers=self.zq_headers, method='POST')
            if draw_data['status'] != 'success':
                print(draw_data['message'])
            else:
                print(f"--{draw_data['message']}---{draw_data['data'].get('prizename')}")

    # 商户专区新
    def shoplist(self):
        task_url = 'https://fission-events.ccbft.com/Component/task/lists/224/8ZWXBM3w'
        tasks_data = self.send_request(task_url, headers=self.zq_headers)
        self.sleep()
        if tasks_data['status'] != 'success':
            print(tasks_data['message'])
        else:
            task_list = tasks_data['data'].get('userTask')
            for value in task_list:
                complete_status = value['finish']
                if complete_status == 1:
                    print('--已完成该任务，继续浏览下一个任务')
                    continue
                task_id = value['id']
                do_url = 'https://fission-events.ccbft.com/Component/task/do/224/8ZWXBM3w'
                payload = {"id": task_id}
                do_data = self.send_request(do_url, headers=self.zq_headers, data=payload, method='POST')
                if do_data['status'] != 'success':
                    print(do_data['message'])
                    continue
                print('--浏览完成')
                time.sleep(3)
            print('--已完成全部任务，去掷骰子')
            time.sleep(3)
            self.throw()

    def throw(self):
        query_url = 'https://fission-events.ccbft.com/activity/dmspshzq/getIndex/224/8ZWXBM3w'
        query_data = self.send_request(query_url, headers=self.zq_headers)
        if query_data['status'] != 'success':
            print(query_data['message'])
        else:
            remain_num = query_data['data'].get('remain_num')
            if remain_num == '0':
                return print('当前没有骰子了')
            self.sleep()
            num = int(remain_num)
            draw_url = 'https://fission-events.ccbft.com/activity/dmspshzq/drawPrize/224/8ZWXBM3w'
            payload = {}
            prizes = []
            for _ in range(num):
                draw_data = self.send_request(draw_url, headers=self.zq_headers, data=payload, method='POST')
                if draw_data['status'] != 'success':
                    print(draw_data['message'])
                    continue
                add_step = draw_data['data'].get('add_step')
                current_step = draw_data['data'].get('current_step')
                prize_name = draw_data['data'].get('prize_name')
                prizes.append(f"前进步数:{add_step},当前步数:{current_step}\n获得奖励:{prize_name}")
                time.sleep(3)

            if prizes:
                print('\n'.join(prizes))

    # 消保专区新
    def fire(self):
        num_url = 'https://fission-events.ccbft.com/activity/dmspxbmountain/getUserInfo/224/jmXN4Q3d'
        num_data = self.send_request(num_url, headers=self.zq_headers)
        self.sleep()
        if num_data.get('status') != 'success':
            print(num_data.get('message'))
        else:
            remain_num = num_data['data'].get('remain_num', 0)
            num = int(remain_num)
            if num == 0:
                print('当前剩余游戏次数为0')
                return
            id_url = 'https://fission-events.ccbft.com/activity/dmspxbmountain/startChallenge/224/jmXN4Q3d'
            draw_url = 'https://fission-events.ccbft.com/Component/draw/commonDrawPrize/224/jmXN4Q3d'
            payload = {}
            for _ in range(num):
                id_data = self.send_request(id_url, headers=self.zq_headers, data=payload, method='POST')
                if id_data.get('status') != 'success':
                    print(id_data.get('message'))
                    continue
                game_id = id_data.get('data')
                print('获取成功，开始登山游戏')
                time.sleep(20)
                game_url = 'https://fission-events.ccbft.com/activity/dmspxbmountain/doChallenge/224/jmXN4Q3d'
                payload_game = {"l_id": game_id, "stage": 13, "score": 200}
                msg_data = self.send_request(game_url, headers=self.zq_headers, data=payload_game,
                                             method='POST')
                if msg_data.get('status') != 'success':
                    print(msg_data.get('message'))
                else:
                    draw_payload = {}
                    draw_data = self.send_request(draw_url, headers=self.zq_headers, data=draw_payload,
                                                  method='POST')
                    if draw_data.get('status') != 'success':
                        print(draw_data.get('message'))
                    else:
                        mes = draw_data.get('message')
                        prizename = draw_data.get('data', {}).get('prizename', '')
                        print(f'{mes}  {prizename}')
                        time.sleep(5)

    # 抓娃娃
    def get_doll(self):
        if doll_flag == 0:
            print('已关闭抓娃娃游戏')
            return

        query_url = 'https://fission-events.ccbft.com/Component/draw/getUserCCB/224/03lA76PW'
        draw_url = 'https://fission-events.ccbft.com/Component/draw/dmspCommonCcbDrawPrize/224/03lA76PW'

        # 查询用户当前可用次数
        query_data = self.send_request(query_url, headers=self.zq_headers)
        user_draw_num = query_data.get('data', {}).get('user_day_draw_num', 0)
        remaining_draws = 10 - int(user_draw_num)
        target_draws = 10 - doll_draw
        print(f'--当前剩余游戏次数: {remaining_draws}')

        # 进行游戏
        while remaining_draws > target_draws:
            draw_data = self.send_request(draw_url, headers=self.zq_headers, method='POST')
            if draw_data.get('status') != 'success':
                print(draw_data.get('message', '抓娃娃游戏出错'))
                remaining_draws -= 1
                continue

            prizename = draw_data.get('data', {}).get('prizename', '未知奖品')
            print(f'{draw_data.get("message", "操作结果")}  获得奖品: {prizename}')
            time.sleep(3)
            remaining_draws -= 1

    # 投篮球
    def do_basket(self):
        if basket_flag == 0:
            print('已关闭投篮球游戏')
            return
        index_url = 'https://fission-events.ccbft.com/a/224/eZgpye3y/index?CCB_Chnl=1000181'
        query_url = 'https://fission-events.ccbft.com/activity/dmspdunk/user/224/eZgpye3y'
        requests.get(url=index_url, headers=self.zq_headers)
        query_data = self.send_request(query_url, headers=self.zq_headers)
        remain_daily = query_data.get('data', {}).get('remain_daily_times')
        num = 5 - basket_draw
        print(f'--当前剩余游戏次数: {remain_daily}')
        self.sleep()

        while remain_daily > num:
            id_url = 'https://fission-events.ccbft.com/activity/dmspdunk/start/224/eZgpye3y'
            id_data = self.send_request(id_url, headers=self.zq_headers, method='POST')

            if id_data.get('status') != 'success':
                print(id_data.get('message'))
                continue
            game_id = id_data.get('data', {}).get('id')
            time.sleep(5)
            activity_url = f'https://fission-events.ccbft.com/activity/dmspdunk/scene/224/eZgpye3y?id={game_id}'
            activity_data = self.send_request(activity_url, headers=self.zq_headers)
            remain_times = activity_data.get('data', {}).get('remain_times')
            basket_num = int(remain_times)  # 篮球数量
            while basket_num > 0:
                dogame_url = 'https://fission-events.ccbft.com/activity/dmspdunk/shot/224/eZgpye3y'
                payload = {'id': game_id}
                dogeme_data = self.send_request(dogame_url, headers=self.zq_headers, data=payload, method='POST')
                if dogeme_data.get('status') != 'success':
                    print(dogeme_data.get('message'))
                    continue
                win_times = dogeme_data.get('data', {}).get('win_times')  # 投中数量
                got_ccb = dogeme_data.get('data', {}).get('got_ccb')  # 获得cc豆
                print(f'当前投中篮球数量: {win_times}')

                if basket_num == 1:
                    print(f'游戏结束,获得cc豆数量: {got_ccb}')
                time.sleep(2.5)
                basket_num -= 1
            remain_daily -= 1

    # 开盲盒
    def open_box(self):
        if box_flag == 0:
            print('已关闭开盲盒')
            return

        # 获取盲盒类型信息
        type_url = 'https://fission-events.ccbft.com/activity/dmspblindbox/index/224/xZ4JKaPl'
        type_data = self.send_request(type_url, headers=self.zq_headers)
        self.sleep()

        # 解析盲盒类型数据
        types = type_data.get('data', [])
        selected_box = next((item for item in types if item['pot_id'] == box_id), None)

        if not selected_box:
            print("未找到对应盲盒种类")
            return

        print(f'当前盲盒种类: [{selected_box["pot_name"]}], 需消耗: {selected_box["draw_one_ccb"]}cc豆')
        self.process_opening(selected_box['pot_id'])

    def process_opening(self, pot_id):
        # 获取用户当前可用次数
        num_url = 'https://fission-events.ccbft.com/Component/draw/getUserCCB/224/xZ4JKaPl'
        num_data = self.send_request(num_url, headers=self.zq_headers)
        self.sleep()

        # 解析可用次数
        draw_num = int(num_data.get('data', {}).get('draw_day_max_num', 0))
        user_num = int(num_data.get('data', {}).get('user_day_draw_num', 0))
        surplus_num = draw_num - user_num

        print(f'--当前可用开盲盒次数: {surplus_num}')

        # 开始开盲盒
        while surplus_num > (draw_num - box_draw):
            open_url = 'https://fission-events.ccbft.com/activity/dmspblindbox/draw/224/xZ4JKaPl'
            open_data = self.send_request(open_url, headers=self.zq_headers, data={"pot_id": pot_id},
                                          method='POST')

            if open_data.get('status') != 'success':
                print(open_data.get('message', '开盲盒失败'))
                surplus_num -= 1
                continue

            prizename = open_data.get('data', {}).get('prizename', '未知物品')
            print(f'开盲盒获得: {prizename}')
            time.sleep(3)
            surplus_num -= 1

    # 查询cc豆及过期cc豆时间
    def get_user_ccd(self):
        urls = {
            'current_ccd': f'https://m3.dmsp.ccb.com/api/businessCenter/user/getUserCCD?zhc_token={self.zhc_token}',
            'expired_ccd': f'https://m3.dmsp.ccb.com/api/businessCenter/user/getUserCCDExpired?zhc_token={self.zhc_token}'
        }
        ccd_data = {}

        for key, url in urls.items():
            try:
                response = self.send_request(url, headers=self.base_header, data={}, method='POST')
                self.sleep()  # Assuming this is a custom method to delay between requests
                if response['code'] != 200:
                    raise Exception(f"Error fetching {key}: {response['message']}")
                ccd_data[key] = response['data']
            except Exception as e:
                print(f"An exception occurred: {e}")
                return  # Early return on failure

        current_count = ccd_data['current_ccd'].get('userCCBeanInfo', {}).get('count', 'unknown')
        expired_count = ccd_data['expired_ccd'].get('userCCBeanExpiredInfo', {}).get('count', 'unknown')
        expire_date_str = ccd_data['expired_ccd'].get('userCCBeanExpiredInfo', {}).get('expireDate', '')

        if expire_date_str:
            expire_date = datetime.fromisoformat(expire_date_str)
            formatted_date = expire_date.strftime('%Y-%m-%d %H:%M:%S')
            print(f'\n当前cc豆: {current_count}，有 {expired_count} cc豆将于 {formatted_date} 过期。')


def getEnv(key):  # line:343
    env_str = os.getenv(key)  # line:344
    if env_str is None:  # line:345
        print(f'青龙变量【{key}】没有获取到!自动退出')  # line:346
        exit()
    try:  # line:348
        env_str = json.loads(
            env_str.replace("'", '"').replace("\n", "").replace(" ", "").replace("\t", ""))  # line:349
        return env_str  # line:350
    except Exception as e:  # line:351
        print(f'请检查变量[{key}]参数是否填写正确')  # line:354

if __name__ == "__main__":
    common.check_cloud("hook_ccb",1.0)
    # cookies = getEnv("hook_ccb")
    cookies = [{
        "deviceid": "7F94989D-1081-4307-A5BE-9312D947EC03",
        "meb_id": "YSM202205192855618",
        "phone": "13183087668",
        "token": "MnFLQjFtTE5renBIMm10WmRlbVpoOW53S25qUTRrR2hjd3ZxTEpYUjU5byUzRDp5UThhVW9vY1B3YkFrZ01jSWV1MG41OFNCckp4Z3FGREF4VDVlMUxOd0h3JTNE",
        "cookie": "XSRF-TOKEN=eyJpdiI6ImI5MXo5RXhvcldRcjF2S21wMVVqSFE9PSIsInZhbHVlIjoiVjZlVXFMZ1l5VVlrT2dEbnZyb2J2L1Zid1l0ZVUwN05CREdUYnBicFNJNUl5cDRJMDB1SXd5UnA0ODRQSFBqYzgwaG9IdCt3S2d1enoraHozQUMrbkQxVXE5ZFBmNHYvTEMvQnNpL2UrSkwxRUFuVW9NOHRlUVI2NUtTNWFaczYiLCJtYWMiOiJlZjMwNmE4ZWNhYmI0MTlhNTAyNGEzOTIxMGU0ZDRlMjYyZmQ4M2E2NjY2MmZkOTk3OTQwYjY3ZjExMjI2Zjc0IiwidGFnIjoiIn0%3D; _ck_bbq_224=eyJpdiI6IjhuYW1SUnp3YXorT0ZKbnh4VXAvc1E9PSIsInZhbHVlIjoiSDFxRmU4RjBmY25RdncwMGZzb1NvK1Q3TXR6dFRER085aDBQRU9BTWNSYlJmSnFscFVZaFkwRlZic2xxWlNDSVFIL3pHNWdPbklaUnA5NVFFZytzYVJxaVZVZ2owQ04xUytwdExsY290aExGRjljckduWk5yaFNwUFNDWW5iZk4iLCJtYWMiOiIxODhhMzlhM2E3MzUyNDk4M2ZiNjk4NDc2ODZhYjQ5ODNlNzEyZTE1ODY1NWY3M2JjNGE3YjVkNjYxMWM0ZTgxIiwidGFnIjoiIn0%3D; _session=eyJpdiI6Ik1oRDYwM3lUOXd5c0ZobEgrRmtDL2c9PSIsInZhbHVlIjoiVy9IQUwxWk8wNEI5Qm9JUW43WTdWbnFvZVBNTkk5ZUtvaGRwbTlwblNjVFVzNHlCSDFCVEovb2tnR01uaG1lbS8yMm5jSVpRcWF2S2dtZjBySG5oU1dNa3Uyd2RkeWxhYld4YlF3RE93cnFJeVNKckJKZm15YndQb0JqM1Z1M2EiLCJtYWMiOiI4MjE2ZDM0MDI2M2MyYWFjZWY0MjE1MjEyM2MyMmFiYmY0MGI0NTVhZjFmNjE3YTBlZjYwNzY4OGM2MWNkNzhlIiwidGFnIjoiIn0%3D; uid=CgIAAmWOZh6YBwQSV+kiAg==; zc_mcpcxkuz9d3f6bey=%7B%22sid%22%3A%20%221703830500383_531711810951041%22%2C%22updated%22%3A%201703831068965%2C%22info%22%3A%201703632055674%2C%22superProperty%22%3A%20%22%7B%5C%22app_id%5C%22%3A%20%5C%22mcpcxkuz9d3f6bey%5C%22%2C%5C%22CmAvy_ID%5C%22%3A%20%5C%22AP010202208051029712%5C%22%2C%5C%22DEVICE_MODEL%5C%22%3A%20%5C%22ca0e16bf-f170-4c54-a809-053628fa2a87%5C%22%2C%5C%22USER_AGENT%5C%22%3A%20%5C%22Mozilla%2F5.0%20(iPhone%3B%20CPU%20iPhone%20OS%2015_4_1%20like%20Mac%20OS%20X)%20AppleWebKit%2F605.1.15%20(KHTML%2C%20like%20Gecko)%20Mobile%2F15E148%20CCBSDK%2F2.4.0%2FCloudMercWebView%2FUnionPay%2F1.0%20CCBLoongPay%5C%22%2C%5C%22Ext_Ad_Mpng_Id%5C%22%3A%20%5C%220000000000000009%5C%22%2C%5C%22SHARE_USER_ID%5C%22%3A%20%5C%22%5C%22%2C%5C%22SHARE_DEPTH%5C%22%3A%20%5C%22%5C%22%2C%5C%22OS%5C%22%3A%20%5C%22jhsh%5C%22%2C%5C%22screen_orientation%5C%22%3A%20%5C%22%5C%22%2C%5C%22CmAvy_EmpID%5C%22%3A%20%5C%22%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22event.ccbft.com%22%7D; zc_did=%7B%22did%22%3A%20%2218c6fc954b11e7d-0bfece4fb0934c8-15194719-505c8-18c6fc954b21d68%22%7D"
    }]
    print(f"建行cc豆共获取到{len(cookies)}个账号")
    for i, cookie in enumerate(cookies, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        CCD(cookie).auto_login()
        print("\n随机等待5-10s进行下一个账号")
        time.sleep(random.randint(5, 10))
