# import mysql.connector as cnt
# from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
# import unicodedata
# from collections import defaultdict
# from datetime import time
#
# # mydb = cnt.connect(
# #     host="139.162.45.23",
# #     user="root",
# #     passwd="duydq",
# #     database="chatbot_olympic"
# # )
# mydb = cnt.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="chatbot_olympic"
# )
# mycursor = mydb.cursor()
#
# list_top_1 = ['barcelona', 'liverpool', 'chelsea', 'paris saint-germain', 'fc bayern munchen',
#               'manchester city', 'juventus', 'Atlético de Madrid', 'Real Madrid',
#               'manchester united', 'arsenal']
# list_top_2 = ['tottenham', 'atlético madrid']

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


a = [1]
a.extend([None, None])

b, c = a[:2]
print(b)
print(c)
