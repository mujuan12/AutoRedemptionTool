import requests
from bs4 import BeautifulSoup
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

    print(uids)
    print(dhms)

    for uid in uids:
        print(f"昵称：{uid[0]}")
        for dhm in dhms:
            res = simulate_submit_event(uid=uid[1], dhm=dhm)
            print(f'\t·兑换码:{dhm}，状态:{res}')


reward()
