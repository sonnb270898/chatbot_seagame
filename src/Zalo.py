import pandas as pd
import time
import pickle
from src.nlp import NER
from flask import Flask, request
from utils.regex_datetime import *
from src.boardcast.broadcast import ZaloOAInfo, ZaloOAClient
import unicodedata
from query.query_database import *
from query.query_string import *
import os

date_now = 4
month_now = 8
year_now = 2016

zalo_info = ZaloOAInfo(oa_id="<Enter your oa_id here>", secret_key="<Enter your token here>")
zalo_oa_client = ZaloOAClient(zalo_info)

s_schedule = ['lịch thi đấu', 'thời gian', 'thời gian thi đấu']
s_result = ['kết quả']
s_define = ['seagame', 'seagames', 'seagames là gì', 'seagame là gì', 'seagames là gì?',
            'seagame là gì?', 'định nghĩa seagames', 'định nghĩa seagame', 'định nghĩa về seagames',
            'định nghĩa về seagame']
s_mascot = ['linh vật', 'con vật', 'biểu tượng', 'đại diện']
s_host = ['đăng cai', 'tổ chức', 'chủ nhà', 'đơn vị tổ chức']
s_ranking = ['bảng xếp hạng', 'bảng tổng sắp', 'huy chương']
file_name = 'svm_model_ver2.sav'
loaded_model = pickle.load(open(file_name, 'rb'))
app = Flask(__name__)


# mydb = cnt.connect(
#     host="139.162.45.23",
#     user="root",
#     passwd="duydq",
#     database="chatbot_olympic"
# )
# mycursor = mydb.cursor()
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
    date_start, date_stop, intent, ner_country_1, ner_country_2, ner_sport, ner_athele, reg = extract(
        message)
    print(intent)
    print(ner_athele)
    print(ner_country_1)
    print(ner_country_2)
    print(ner_sport)
    print(date_start)
    print(date_stop)
    if intent == 'define':
        message_response = class_define()
        return message_response, intent
    elif intent == 'host':
        message_response = class_host()
        return message_response, intent
    elif intent == 'list_sports':
        message_response = class_list_of_sports()
        return message_response, intent
    elif intent == 'list_countries':
        message_response = class_number_of_countries()
        return message_response, intent
    elif intent == 'mascot':
        message_response = class_mascot()
        return message_response, intent
    elif intent == 'rank':
        message_response = class_ranking()
        return message_response, intent
    elif intent == 'athele':
        message_response = class_athele(ner_athele)
        return message_response, intent
    elif intent == 'schedule':
        message_response = class_schedule(date_start, date_stop, reg)
        return message_response, intent
    elif intent == 'result':
        message_response = class_result(date_start, date_stop, reg)
        return message_response, intent
    elif intent == 'chuaro':
        return 'Mời bạn nhập lại câu hỏi', intent
    else:
        return 'Mời bạn nhập lại câu hỏi', intent


def btn_attachment(intent):
    if intent == 'athele':
        attachment = [
            {
                "title": "Nguyễn Quang Hải",
                "type": "oa.query.show",
                "payload": "Nguyễn Quang Hải"
            },
            {
                "title": "Nguyễn Công Phượng",
                "type": "oa.query.show",
                "payload": "Nguyễn Công Phượng"
            },
            {
                "title": "Lương Xuân Trường",
                "type": "oa.query.show",
                "payload": "Lương Xuân Trường"
            }

        ]
    elif intent == 'define':
        attachment = [
            {
                "title": "Linh vật Seagames",
                "type": "oa.query.show",
                "payload": "Linh vật Seagames"
            },
            {
                "title": "Quốc gia chủ nhà",
                "type": "oa.query.show",
                "payload": "Quốc gia chủ nhà"
            },
            {
                "title": "Danh sách quốc gia",
                "type": "oa.query.show",
                "payload": "Danh sách quốc gia"
            }
        ]
    elif intent == 'schedule' or intent == 'result':
        attachment = [
            {
                "title": "Lịch thi đấu hôm nay",
                "type": "oa.query.show",
                "payload": "Lịch thi đấu hôm nay"
            },
            {
                "title": "Kết quả thi đấu hôm nay",
                "type": "oa.query.show",
                "payload": "Kết quả thi đấu hôm nay"
            },
            {
                "title": "Bảng xếp hạng",
                "type": "oa.query.show",
                "payload": "Bảng xếp hạng"
            }

        ]
    else:
        attachment = []
    return attachment


def reply_msg_btn(uid, ans, intent):
    message = ans if ans != '' else '....'
    attachment = btn_attachment(intent)
    if intent == 'define' or intent == 'schedule' or intent == 'result':
        data = {
            "recipient": {
                "user_id": uid
            },
            "message": {
                "text": message,
                "attachment": {
                    "type": "template",
                    "payload": {
                        "buttons": attachment
                    }
                }
            }
        }
    else:
        data = {
            "recipient": {
                "user_id": uid
            },
            "message": {
                "text": message
            }
        }
    params = {'data': data}
    send_text_message = zalo_oa_client.post('message', params)
    print(send_text_message)


def reply_msg(uid, ans):
    message = ans if ans != '' else '....'
    data = {
        "recipient": {
            "user_id": uid
        },
        "message": {
            "text": message
        }
    }
    params = {'data': data}
    send_text_message = zalo_oa_client.post('message', params)
    print(send_text_message)


@app.route('/webhook/', methods=['POST'])
def user_send_mess():
    data = request.json
    print(data)
    print(type(data))
    hello = '''
Chatbot cung cấp thông tin về Seagames với các đạng câu hỏi:
 - Seagames là gì?
 - Linh vật Seagames
 - Chủ nhà đăng cai tổ chức
 - Danh sách quốc gia tham dự
 - Danh sách bộ môn thi đấu
 - Thông tin về vận động viên
 - Bảng xếp hạng
 - Lịch thi đấu
 - Kết quả trận đấu
    '''
    if data.get('event_name') == 'follow':
        reply_msg(data['follower']['id'], hello)
    if data.get("event_name") == "user_send_text":
        if data.get('message', '') != '':
            if isinstance(data['message'], dict):  # hàm này kiểm tra data r mà vẫn đéo
                str = data['message'].get('text', '')
                ans, intent = response(str)
                x = int(len(ans) / 2000)
                for i in range(x):
                    reply_msg(data['sender']['id'], ans[i * 2000:i * 2000 + 1999])
                    time.sleep(0.5)
                reply_msg_btn(data['sender']['id'], ans[x * 2000:len(ans)], intent)
            else:
                return 'ok'
        return 'ok'
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 4444)))
