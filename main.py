import requests
from bs4 import BeautifulSoup
import time
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
    # url_encoded_text = quote(dhm)
    # url_encoded_text = dhm

    payload = {
        'uid': uid,
        'code': dhm,
        'token': 0
    }
    newurl = url + "?uid=" + uid + "&code=" + dhm
    response = requests.post(newurl, data=payload)
    if response is None:
        print("空")
    print(response.text)
    return response.json()


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
    uids = Open('uid.txt')
    dhms_LongTime = Open('dhm_LongTime')
    dhms_limited = Open('dhm_limited')

    data = {}
    msg = ""

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
        for dhm in dhms_limited:
            res = simulate_submit_event(uid=uid[1], dhm=dhm)
            time.sleep(0.3)

            status.append(f'兑换码:{dhm}\n\n\t\t状态:{res["msg"]}')
            print(f'\t·兑换码:{dhm}，状态:{res}')
        for stat in status:
            tmp = tmp + "\t{}\n\n".format(stat)

        msg = msg + tmp

        modifyUidIsRewardLongDhm(uid=uid[1])

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


def modifyUidIsRewardLongDhm(uid):
    with open('uid.txt', 'r+', encoding='utf-8') as file:
        # 读取文件的每一行
        lines = file.readlines()

        # 遍历每一行
        for i, line in enumerate(lines):
            # 判断是否是指定的行
            if uid in line:
                # 在该行的末尾追加数据
                index = line.find(' ', line.find(' ') + 1)
                new_line = line[:index]
                new_line += ' true\n'
                # 将修改后的行写回文件
                lines[i] = new_line
                break

        # 将修改后的内容写回文件
        file.seek(0)
        file.writelines(lines)

        # 关闭文件
        file.close()


data = reward()
sendMsg(data=data)
