import time
from datetime import datetime
import mysql.connector as cnt
from src.utils.pattern.regex_datetime import *
from collections import defaultdict
import schedule
import redis
from flask import Flask
import requests


#----------------database--------
mydb = cnt.connect(
    host="localhost",
    user="root",
    passwd="",
    database="chatbot_olympic"
)
mycursor = mydb.cursor()

#----------------redis-----------
r = redis.Redis(host='localhost', port=6379, db=0)

#---------------Flask------------
app = Flask(__name__)
VERIFY_TOKEN = 'maxacminh'
TOKEN = '?access_token=EAAM1r77ZBZAyEBAONrekNsQHxSDr8vwyU3Nlldo0D9zMrgv13mgiP3KJ2aIMajtiHTNGr7wmWqqs6zwT2ydZCpSJJ2agbDar9Ro02zpLX276ZA64foPn90xVkgUEzqKwm0wSYttuQ5XR7473uAyydQg5W8LeX7ZA6YtFtZCpApkQZDZD'
URL = 'https://graph.facebook.com/v4.0/me/'

#--------------get flwers---------
query = "SELECT uid FROM user"
mycursor.execute(query)
myresult = mycursor.fetchall()

r.flushall()
for user in myresult:
    r.rpush('followers',user[0])
followers = r.lrange('followers','0','-1')

print(followers)
print('------------------')





def cvt_1_to_2(so):
    if so <10:
        return '0'+str(so)
    else:
        return str(so)
def gettime(time):
    month = cvt_1_to_2(time.month)
    day   = cvt_1_to_2(time.day)
    hour  = cvt_1_to_2(time.hour)
    minute = cvt_1_to_2(time.minute)
    return hour+':'+minute+' '+day+'/'+month

def broadcast(ans):
    intent = 'schedule'
    followers = r.lrange('followers', '0', '-1')
    if ans != "Không có trận đấu nào":
        for user in followers:
            reply_msg(user,ans,intent)


def reply_msg(uid, ans,intent):
    print(uid)
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

def respone():
    # now = datetime.datetime.now()
    # next = now + timedelta(seconds=1800)
    now = datetime.datetime(2016,8,4,15,45,0)
    next = datetime.datetime(2016, 8, 4, 16, 45, 0)
    query = "SELECT * FROM schedule WHERE time>={} AND time<{} ".format(now.timestamp(), next.timestamp())
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    dict_match = defaultdict(list)

    if len(myresult) != 0:
        for x in myresult:
            dict_match[x[2]].append((x[1], x[4], x[5], x[7]))
        message = ''
        dem = 1
        for sport in dict_match:
            dict_match_sport = defaultdict(list)
            for i in dict_match[sport]:
                dict_match_sport[i[0]].append((i[1], i[2], i[3]))
            title = '\n➤ ' + sport.title() + ' :\n'
            c = 1
            c1 = ''
            for i in dict_match_sport:
                result = ''
                time = datetime.datetime.fromtimestamp(float(dict_match_sport[i][0][2]))
                for j in dict_match_sport[i]:
                    result = result + '{}({}), '.format(j[0].title(), j[1])
                content = '  ➵ ' + gettime(time) + ' ' + result[:-2] + '\n'
                c += 1
                c1 = c1 + content
                if c == 5:
                    break
            ketqua = title + c1
            message = message + ketqua
            dem = dem + 1
            if dem == 4:
                break
        return (message+'\n Xem thêm : ☞  '+'link')
    else:
        return "Không có trận đấu nào"
broadcast(respone())
schedule.every(30).minutes.do(broadcast,respone())
while True:
    schedule.run_pending()
    time.sleep(1)
