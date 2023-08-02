import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote
import json
# -*- coding: utf-8 -*-


giftCodeUrl = "http://statistics.pandadastudio.com/player/giftCodeView"
infoUrl = r"E:\Microsoft Edge Downloads\uid.url"
rewardUrl = "http://statistics_1.pandadastudio.com/player/giftCode"


def getUid():
    response = requests.get(infoUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    infoList = soup.find('textarea')
    # print(response.text)
    if "可可姐" in response.text:
        print(1111111)
    print(infoList)


def simulate_submit_event(uid, dhm):
    url = "http://statistics.pandadastudio.com/player/giftCode" if len(
        uid) != 12 else "http://statistics_1.pandadastudio.com/player/giftCode"

    # 将中文转换为 URL 编码
    #url_encoded_text = quote(dhm)
    #url_encoded_text = dhm

    payload = {
        'uid': uid,
        'code': dhm,
        'token': 0
    }
    newurl = url + "?uid=" + uid + "&code=" + dhm
    response = requests.post(newurl, data=payload)
    if response is None:
        print("空")
    return response.json()


def Open(filename):
    data_list = []
    with open(filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if ' ' in line:
                elements = line.split(' ')
                if len(elements) == 2:
                    data_list.append((elements[0], elements[1]))
            else:
                data_list.append(line)
    return data_list


def reward():
    uids = Open('uid.txt')
    dhms = Open('dhm.txt')

    data = {}
    msg = ""

    for uid in uids:
        flag = 0
        print(f"昵称：{uid[0]}")
        status = []
        tmp = "### {}\n\n".format(uid[0])
        for dhm in dhms:
            if dhm == "长期:" or dhm == "限时:":
                if dhm == "限时:":
                    flag = 1
                continue
            res = simulate_submit_event(uid=uid[1], dhm=dhm)

            if flag:
                status.append(f'兑换码:{dhm},\n\n状态:{res}')
            else:
                if res['code'] != 425:
                    status.append(f'兑换码:{dhm}，\n\n状态:{res}')
            print(f'\t·兑换码:{dhm}，状态:{res}')
        for stat in status:
            tmp = tmp + "\t{}\n\n".format(stat)
            msg = msg + tmp
        #data[uid[0]] = tmp
    #print(data)
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


data = reward()
sendMsg(data=data)