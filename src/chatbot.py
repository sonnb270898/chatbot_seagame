"""
Chatbot for Fashion
"""
import os
from flask import Flask, request
from src.script.ZaloAPI import ZaloOAInfo,ZaloOAClient
from src.config import FACEBOOK_API_ENDPOINT,FACEBOOK_TOKEN_PAGE,OA_ID,SECRET_KEY,ZALO_TOKEN,API_OA_LINK
from src.script.ZaloAPI import ZaloOAInfo,ZaloBaseClient,ZaloOAClient
import json

try:
    from utils.logger import log_debug, log_error
    from dialog import Dialog
    from config import FACEBOOK_WEBHOOK_VERIFY_TOKEN
except ImportError:
    # for develop
    from src.utils.logger import log_debug, log_error
    from src.dialog import Dialog
    from src.config import FACEBOOK_WEBHOOK_VERIFY_TOKEN

# def checksource(data):
#     if data.get('object'):
#         return 'facebook'
#     else:
#         return 'zalo'

zalo_info = ZaloOAInfo(oa_id=OA_ID, secret_key=SECRET_KEY)
zalo_oa_client = ZaloOAClient(zalo_info)

app = Flask(__name__)



class Chatbot:
    """
    Class handle webhook from facebook, zalo and ...
    """

    def __init__(self):
        self.dialog = Dialog()

    def handle(self, data):
        """
        Handle message from user
        """
        # endpoint for processing incoming messaging events
        # log_debug(data)
        log_debug(data)
        if data.get("source") == "facebook":
            if data.get("object") == "page":
                for entry in data.get("entry"):
                    for messaging_event in entry['messaging']:
                        log_debug('handle - souce = "facebook"')
                        log_debug('+++++++++++++++++++++++++++++++++++++++')
                        self.handle_message_facebook(messaging_event)

            return
        if data.get("source") == "zalo":
            if data.get("event_name") == "user_send_text":
                if data.get('message'):
                    log_debug('handle - source = "zalo"')
                    log_debug('+++++++++++++++++++++++++++++++++++++++')
                    self.handle_message_zalo(data)
            return

    def handle_message_facebook(self, messaging_event):
        """
        handle type of message
        """
        message = ""
        # the facebook ID of the person sending message
        user_id = messaging_event['sender']['id']
        # the recipient's ID, which should be your page's facebook ID
        page_id = messaging_event['recipient']['id']
        if messaging_event.get('message'):  # someone sent us a message
            # # quick rely
            # message_quick_reply = messaging_event['message'].get('quick_reply')
            # if message_quick_reply:
            #     message = message_quick_reply['payload']
            # the message's text
            message_text = messaging_event['message'].get('text')
            if message_text:
                message = message_text

        # user clicked/tapped "postback" button in earlier message
        if messaging_event.get('postback'):
            message = messaging_event['postback']['payload']

        self.dialog.handle_message(
            user_id=user_id, input_text=message, page_id=page_id, source="facebook")

    def handle_message_zalo(self,data):
        message = ""
        user_id = data['sender']['id']
        page_id = data['recipient']['id']
        if data.get('message'):
            message_text = data['message'].get('text')
            if message_text:
                message = message_text
        self.dialog.handle_message(
            user_id=user_id, input_text=message, page_id=page_id, source="zalo")


chatbot = Chatbot()


@app.route('/webhook/facebook', methods=['GET'])
def webhook_auth():
    """
    Authen webhook
    """
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FACEBOOK_WEBHOOK_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/webhook/facebook', methods=['POST'])
def webhook_handle():
    try:
        data = request.get_json()
        data["source"] = "facebook"
        chatbot.handle(data)
    except Exception as ex:
        log_error(str(ex))
    return "ok", 200

@app.route('/webhook/zalo',methods = ['POST'])
def user_send_mess():
    try:
        data = request.get_json()
        data["source"] = "zalo"
        chatbot.handle(data)
    except Exception as ex:
        log_error(str(ex))
    return "ok", 200


if __name__ == '__main__':
    app.run(
        host=os.environ.get('LISTEN_HOST', '0.0.0.0'),
        port=os.environ.get('LISTEN_PORT', 4444),
        debug=False,
        load_dotenv=True
    )
