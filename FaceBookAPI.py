import json
import requests
from flask import Flask, request
from query.query_database import *
from query.query_string import *
import pickle
import pandas as pd
import time
import os
s_schedule = ['lịch thi đấu', 'thời gian', 'thời gian thi đấu']
s_result = ['kết quả']
s_define = ['seagame', 'seagames', 'seagames là gì', 'seagame là gì', 'seagames là gì?', 'seagame là gì?',
            'định nghĩa seagames', 'định nghĩa seagame', 'định nghĩa về seagames', 'định nghĩa về seagame']
s_mascot = ['linh vật', 'con vật', 'biểu tượng', 'đại diện']
s_host = ['đăng cai', 'tổ chức', 'chủ nhà', 'đơn vị tổ chức']
s_ranking = ['bảng xếp hạng', 'bảng tổng sắp', 'huy chương']
file_name = 'svm_model_ver2.sav'
loaded_model = pickle.load(open(file_name, 'rb'))

def rw_follower():
    with open('follower.txt', 'a+', encoding='utf-8') as f:
        for i in new_followers:
            f.write(str(i) + '\n')
    new_followers.clear()
    with open('follower.txt', 'r', encoding='utf-8') as f:
        followers = f.read().strip().split('\n')
    return new_followers,followers

app = Flask(__name__)
VERIFY_TOKEN = 'maxacminh'
TOKEN = '<Enter your token here>'
URL = 'https://graph.facebook.com/v4.0/me/'


def extract(question):
    question = unicodedata.normalize("NFC", question.lower())
    ngay, thang, nam, hom, thu, tuan, buoi = regex(question)
    date_start, date_stop = ner(ngay, thang, nam, hom, tuan, thu, buoi)
    if date_start == 0 and date_stop == 0:
        date_start, date_stop = ner(0, 0, 0, 'hôm nay', None, None, None)
    aaa = NER(question)
    reg = aaa.entities
    is_country = aaa.entities['is_country']
    is_sport = aaa.entities['is_sport']
    is_name = aaa.entities['is_name']
    if len(is_country) == 0:
        ner_country_1 = None
        ner_country_2 = None
    elif len(is_country) == 1:
        ner_country_1 = is_country[0]
        ner_country_2 = None
    else:
        ner_country_1 = is_country[0]
        ner_country_2 = is_country[1]

    if len(is_name) == 0:
        ner_athele = None
    else:
        ner_athele = is_name[0]
        question = question.replace(ner_athele, 'vận động viên')

    if len(is_sport) == 0:
        ner_sport = None
    else:
        ner_sport = is_sport[0]
        question = question.replace(ner_sport, ner_sport + ' bộ môn')
    print(question)
    ##INTENT
    df = pd.DataFrame([{'feature': question}])
    intent = loaded_model.predict(df['feature'])[0].strip()
    # Từ khóa
    for i in s_schedule:
        if i.strip().lower() in question.strip().lower():
            intent = 'schedule'
            break
    if ner_athele != None:
        intent = 'athele'
    a = loaded_model.predict_proba(df["feature"])
    print(a)
    if intent == 'schedule' or intent == 'result':
        if max(a[0]) < 0.69:
            intent = 'chuaro'
    elif intent == 'rank':
        if ner_sport != None:
            intent = 'schedule'
    for i in s_define:
        if i.strip().lower() == question.strip().lower():
            intent = 'define'

    for i in s_mascot:
        if i.strip().lower() in question.strip().lower():
            intent = 'mascot'

    for i in s_result:
        if i.strip().lower() in question.strip().lower():
            intent = 'result'

    for i in s_ranking:
        if i.strip().lower() in question.strip().lower():
            intent = 'rank'

    for i in s_host:
        if i.strip().lower() in question.strip().lower():
            intent = 'host'
    if question.strip().lower() == 'quốc gia':
        intent = 'list_countries'
    if question.strip().lower() == 'kết quả tổng sắp':
        intent = 'rank'
    return date_start, date_stop, intent, ner_country_1, ner_country_2, ner_sport, ner_athele, reg


def response(message):
    date_start, date_stop, intent, ner_country_1, ner_country_2, ner_sport, ner_athele, reg = extract(message)
    # print(intent)
    # print(ner_athele)
    # print(ner_country_1)
    # print(ner_country_2)
    # print(ner_sport)
    # print(date_start)
    # print(date_stop)
    if intent == 'define':
        message_response = class_define()
        return message_response
    elif intent == 'host':
        message_response = class_host()
        return message_response
    elif intent == 'list_sports':
        message_response = class_list_of_sports()
        return message_response
    elif intent == 'list_countries':
        message_response = class_number_of_countries()
        return message_response
    elif intent == 'mascot':
        message_response = class_mascot()
        return message_response
    elif intent == 'rank':
        message_response = class_ranking()
        return message_response
    elif intent == 'athele':
        message_response = class_athele(ner_athele)
        return message_response
    elif intent == 'schedule':
        message_response = class_schedule(date_start, date_stop, reg)
        return message_response
    elif intent == 'result':
        message_response = class_result(date_start, date_stop, reg)
        return message_response
    elif intent == 'chuaro':
        return 'Mời bạn nhập lại câu hỏi'
    else:
        return 'Mời bạn nhập lại câu hỏi'


def reply_msg(uid, ans):
    data = {
        "recipient": {
            "id": uid
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": ans,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Red",
                    "payload": "<POSTBACK_PAYLOAD>",
                }, {
                    "content_type": "text",
                    "title": "Green",
                    "payload": "<POSTBACK_PAYLOAD>",
                }
            ]
        }
    }
    endpoint = "%s%s%s" % (URL, 'messages', TOKEN)

    headers = {
        'access_token': TOKEN,
        'content-type': 'application/json'
    }
    try:
        res = requests.post(endpoint, json=data, headers=headers)
    except Exception:
        print("exception")
        return 200
    print(res.json())


# def broadcast_msg():
#     # data = {
#     #     "messages": [
#     #         {
#     #             "attachment": {
#     #                 "type": "template",
#     #                 "payload": {
#     #                     "template_type": "generic",
#     #                     "elements": [
#     #                         {
#     #                             "title": "Welcome to Our Marketplace!",
#     #                             "image_url": "https://www.facebook.com/jaspers.png",
#     #                             "subtitle": "Fresh fruits and vegetables. Yum.",
#     #                             "buttons": [
#     #                                 {
#     #                                     "type": "web_url",
#     #                                     "url": "https://www.jaspersmarket.com",
#     #                                     "title": "View Website"
#     #                                 }
#     #                             ]
#     #                         }
#     #                     ]
#     #                 }
#     #             }
#     #         }
#     #     ]
#     # }
#     data = {"messages": [
#         {
#             "attachment": {
#                 "type": "template",
#                 "payload": {
#                     "template_type": "generic",
#                     "elements": [
#                         {
#                             "title": "Welcome to Our Marketplace!",
#                             "image_url": "https://www.facebook.com/jaspers.png",
#                             "subtitle": "Fresh fruits and vegetables. Yum.",
#                             "buttons": [
#                                 {
#                                     "type": "web_url",
#                                     "url": "https://www.jaspersmarket.com",
#                                     "title": "View Website"
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             }
#         }
#     ]}
#     # mc_endpoint = "%s%s%s" % (URL, 'message_creatives', TOKEN)
#     # bc_endpoint = "%s%s%s" % (URL, 'broadcast_messages', TOKEN)
#     mc_endpoint = "https://graph.facebook.com/v3.3/me/message_creatives?access_token=EAAM1r77ZBZAyEBAONrekNsQHxSDr8vwyU3Nlldo0D9zMrgv13mgiP3KJ2aIMajtiHTNGr7wmWqqs6zwT2ydZCpSJJ2agbDar9Ro02zpLX276ZA64foPn90xVkgUEzqKwm0wSYttuQ5XR7473uAyydQg5W8LeX7ZA6YtFtZCpApkQZDZD"
#     bc_endpoint = "https://graph.facebook.com/v3.3/me/broadcast_messages?access_token=EAAM1r77ZBZAyEBAONrekNsQHxSDr8vwyU3Nlldo0D9zMrgv13mgiP3KJ2aIMajtiHTNGr7wmWqqs6zwT2ydZCpSJJ2agbDar9Ro02zpLX276ZA64foPn90xVkgUEzqKwm0wSYttuQ5XR7473uAyydQg5W8LeX7ZA6YtFtZCpApkQZDZD"
#     headers = {
#         'access_token': TOKEN,
#         'content-type': 'application/json'
#     }
#     # a = json.dumps(data)
#     try:
#         res = requests.post(mc_endpoint, json=data, headers=headers)
#         message_creative_id = res.json()['message_creative_id']
#         data2 = {
#             "message_creative_id": int(message_creative_id),
#             "notification_type": "SILENT_PUSH",
#             "messaging_type": "MESSAGE_TAG",
#             "tag": "NON_PROMOTIONAL_SUBSCRIPTION"
#         }
#         res = requests.post(bc_endpoint, data=data2, headers=headers)
#     except Exception as ex:
#         print("exception", str(ex))
#         return 200
#     print(res.json())
#     print(res)
# new_followers = []
# followers = []

@app.route('/webhook', methods=['POST'])
def msg():
    global new_followers,followers
    data = request.json
    print(data)
    uid = data['entry'][0]['messaging'][0]['sender']['id']
    # if (uid not in followers):
    #     new_followers.append(uid)
    # if(len(new_followers) == 10):
    #     new_followers,followers = rw_follower()

    if (data['entry'][0]['messaging'][0].get('message', '') != '' or data['entry'][0]['messaging'][0].get('postback', '') != ''):
        message = data['entry'][0]['messaging'][0]['message']['text'] if data['entry'][0]['messaging'][0].get('message', '') else data['entry'][0]['messaging'][0]['postback']['payload']
        print(uid, message)
        ans = response(message)
        x = int(len(ans) / 2000)
        try:
            for i in range(x):
                reply_msg(uid, ans[i * 2000:i * 2000 + 1999])
                time.sleep(0.5)
            reply_msg(uid, ans[x * 2000:len(ans)])
        except Exception:
            return 200
    return 'success'

@app.route('/webhook', methods=['GET'])
def verify():
    data = request.args
    print(data)
    verify = data['hub.verify_token']
    challenge = data['hub.challenge']
    mode = data['hub.mode']
    if (verify == VERIFY_TOKEN and mode == 'subscribe'):
        return challenge
    return 'invalid'

if __name__ == "__main__":
    app.run(debug=True,port=int(os.getenv('PORT', 4444)))

