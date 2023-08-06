import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote
import json

# -*- coding: utf-8 -*-


giftCodeUrl = "http://statistics.pandadastudio.com/player/giftCodeView"
baseInfoUrl = r"http://82.157.236.56:8080/info/"
baseDeleteDhmUrl = "http://82.157.236.56:8080/dhm/delete/"
rewardUrl = "http://statistics_1.pandadastudio.com/player/giftCode"


def getInfo(fileName):
    info_path = baseInfoUrl+fileName
    res = requests.get(url=info_path)

    soup = BeautifulSoup(res.text,'html.parser')
    p_tags = soup.find_all("p")
    lines = []
    info_list = []
    for p in p_tags:
        lines.append(p.text)

    for line in lines:
        if line.isspace():
            continue
        line = line.strip()
        if ' ' in line:
            elements = line.split(' ')
            if len(elements) == 3:
                info_list.append((elements[0], elements[1], elements[2]))
        else:
            info_list.append(line)
    return info_list


def simulate_submit_event(uid, dhm):
    url = "http://statistics.pandadastudio.com/player/giftCode" if len(
        uid) != 12 else "http://statistics_1.pandadastudio.com/player/giftCode"

    payload = {
        'uid': uid,
        'code': dhm,
        'token': 0
    }
    newurl = url + "?uid=" + uid + "&code=" + dhm
    response = requests.post(newurl, data=payload).json()
    if response is None:
        print("空")

    return response


def Open(filename):
    data_list = []
    with open(filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.isspace():
                continue
            line = line.strip()
            if ' ' in line:
                elements = line.split(' ')
                if len(elements) == 3:
                    data_list.append((elements[0], elements[1], elements[2]))
            else:
                data_list.append(line)
    file.close()
    return data_list

def reward():
    uids = getInfo("uid")
    dhms_LongTime = getInfo("dhm_LongTime")
    dhms_limited = getInfo('dhm_limited')

    data = {}
    msg = ""
    unUsed_dhm = []

    for uid in uids:
        print(f"昵称：{uid[0]}")
        status = []
        tmp = "### {}\n\n".format(uid[0])
        for dhm in dhms_LongTime:
            if uid[2] == 'true':
                break
            res = simulate_submit_event(uid=uid[1], dhm=dhm)
            time.sleep(0.3)

            #if res['code'] != 425:
            status.append(f'兑换码:{dhm}\n\n\t\t状态:{res["msg"]}')
            print(f'\t·兑换码:{dhm}，状态:{res}')

            if res['code'] != 425 and res['code'] != 0:
                print(1)
                unUsed_dhm.append(dhm)
                dhms_LongTime.remove(dhm)

        for dhm in dhms_limited:
            res = simulate_submit_event(uid=uid[1], dhm=dhm)
            time.sleep(0.3)

            status.append(f'兑换码:{dhm}\n\n\t\t状态:{res["msg"]}')
            print(f'\t·兑换码:{dhm}，状态:{res}')

            if res['code'] != 425 and res['code'] != 0:
                unUsed_dhm.append(dhm)
                dhms_limited.remove(dhm)

        for stat in status:
            tmp = tmp + "\t{}\n\n".format(stat)

        msg = msg + tmp

        modifyUidIsRewardLongDhm(uid=uid[1])

        for dhm in unUsed_dhm:
            # 该兑换码无效或未到时间，删除该兑换码
            delete_path = baseDeleteDhmUrl + dhm
            requests.get(delete_path)
            unUsed_dhm.remove(dhm)
    print(dhms_limited)
    print(dhms_LongTime)

    return msg


def sendMsg(data):
    notifyToken = "SCT218479TQMHt4Eig5ZIuhFRk8h8jOOyj"
    url = "https://sctapi.ftqq.com/{}.send"

    body = {
        "title": "⏰ 兑换结果通知",
        "desp": "{}".format(data)
    }
    requests.post(url.format(notifyToken), data=body)
    print("消息已通过 Serverchan-Turbo 推送，请检查推送结果")

# 修改兑换完长期兑换码的用户的标志位 true
def modifyUidIsRewardLongDhm(uid):
    modify_path = 'http://82.157.236.56:8080/' + uid
    requests.get(modify_path)


data = reward()
sendMsg(data=data)
#getUid()
