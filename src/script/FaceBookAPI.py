import json
import requests
import sys
from flask import Flask, request
sys.path.append('E:/rabiloo/chatbot_zalo_seagames/src/response')
from query import *
from string import *
import pickle
import pandas as pd
import time
import os
import redis

s_schedule = ['lịch thi đấu', 'thời gian', 'thời gian thi đấu']
s_result = ['kết quả']
s_define = ['seagame', 'seagames', 'seagames là gì', 'seagame là gì', 'seagames là gì?', 'seagame là gì?',
            'định nghĩa seagames', 'định nghĩa seagame', 'định nghĩa về seagames', 'định nghĩa về seagame']
s_mascot = ['linh vật', 'con vật', 'biểu tượng', 'đại diện']
s_host = ['đăng cai', 'tổ chức', 'chủ nhà', 'đơn vị tổ chức']
s_ranking = ['bảng xếp hạng', 'bảng tổng sắp', 'huy chương']
file_name = 'svm_model_ver2.sav'
loaded_model = pickle.load(open(file_name, 'rb'))
mydb = cnt.connect(
    host="localhost",
    user="root",
    passwd="",
    database="chatbot_olympic"
)
mycursor = mydb.cursor()

r = redis.Redis(host='localhost', port=6379, db=0)

query = "SELECT uid FROM user"
mycursor.execute(query)
myresult = mycursor.fetchall()

for user in myresult:
    r.rpush('followers',user[0])
# followers = [user[0] for user in myresult]
followers = r.lrange('followers','0','-1')

print(followers)
print('------------------')


app = Flask(__name__)
VERIFY_TOKEN = 'maxacminh'
TOKEN = '?access_token=EAAM1r77ZBZAyEBAONrekNsQHxSDr8vwyU3Nlldo0D9zMrgv13mgiP3KJ2aIMajtiHTNGr7wmWqqs6zwT2ydZCpSJJ2agbDar9Ro02zpLX276ZA64foPn90xVkgUEzqKwm0wSYttuQ5XR7473uAyydQg5W8LeX7ZA6YtFtZCpApkQZDZD'
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
        return message_response,intent
    elif intent == 'host':
        message_response = class_host()
        return message_response,intent
    elif intent == 'list_sports':
        message_response = class_list_of_sports()
        return message_response,intent
    elif intent == 'list_countries':
        message_response = class_number_of_countries()
        return message_response,intent
    elif intent == 'mascot':
        message_response = class_mascot()
        return message_response,intent
    elif intent == 'rank':
        message_response = class_ranking()
        return message_response,intent
    elif intent == 'athele':
        message_response = class_athele(ner_athele)
        return message_response,intent
    elif intent == 'schedule':
        message_response = class_schedule(date_start, date_stop, reg)
        return message_response,intent
    elif intent == 'result':
        message_response = class_result(date_start, date_stop, reg)
        return message_response,intent
    elif intent == 'chuaro':
        return 'Mời bạn nhập lại câu hỏi',intent
    else:
        return 'Mời bạn nhập lại câu hỏi',intent


def reply_msg(uid, ans,intent):
    if intent == 'athele':
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
                        "title": "Nguyễn Công Phượng",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }, {
                        "content_type": "text",
                        "title": "Nguyễn Quang Hải",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }
                ]
            }
        }
    elif intent == 'define':
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
                        "title": "Linh Vật Seagames",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }, {
                        "content_type": "text",
                        "title": "Quốc gia chủ nhà",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }, {
                        "content_type": "text",
                        "title": "Danh sách quốc gia",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }
                ]
            }
        }
    elif intent == 'result' or intent == 'schedule':
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
                        "title": "Lịch thi đấu hôm nay",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }, {
                        "content_type": "text",
                        "title": "Kết quả thi đấu hôm qua",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }, {
                        "content_type": "text",
                        "title": "Bảng xếp hạng",
                        "payload": "<POSTBACK_PAYLOAD>",
                    }
                ]
            }
        }
    else:
        data = {
            "recipient": {
                "id": uid
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": ans,
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

def broadcast(ans):
    intent = 'schedule'
    followers = r.lrange('followers', '0', '-1')
    if ans != "Không có trận đấu nào":
        for user in followers:
            reply_msg(user,ans,intent)

@app.route('/webhook', methods=['POST'])
def msg():
    data = request.json
    print(data)
    uid = data['entry'][0]['messaging'][0]['sender']['id']
    if bytes(uid,'utf-8') not in followers:
        query = "INSERT INTO user(uid) VALUES ('{}')".format(uid)
        mycursor.execute(query)
        mydb.commit()
        r.rpush('followers',uid)
    if (data['entry'][0]['messaging'][0].get('message', '') != '' or data['entry'][0]['messaging'][0].get('postback', '') != ''):
        message = data['entry'][0]['messaging'][0]['message']['text'] if data['entry'][0]['messaging'][0].get('message', '') else data['entry'][0]['messaging'][0]['postback']['payload']
        print(uid, message)
        ans,intent = response(message)
        x = int(len(ans) / 2000)
        try:
            for i in range(x):
                reply_msg(uid, ans[i * 2000:i * 2000 + 1999])
                time.sleep(0.5)
            reply_msg(uid, ans[x * 2000:len(ans)],intent)
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

