"""
Class format text message
"""
import json
import requests
<<<<<<< HEAD
from src.response.messages.message import Mesage
from src.utils.logger import log_debug
from src.config import FACEBOOK_API_ENDPOINT, FACEBOOK_TOKEN_PAGE,OA_ID,SECRET_KEY
from src.script.ZaloAPI import ZaloOAInfo,ZaloOAClient
=======

try:
    from response.messages.message import Mesage
    from utils.logger import log_debug
    from config import FACEBOOK_API_ENDPOINT, FACEBOOK_TOKEN_PAGE
except ImportError:
    from src.response.messages.message import Mesage
    from src.utils.logger import log_debug
    from src.config import FACEBOOK_API_ENDPOINT, FACEBOOK_TOKEN_PAGE
>>>>>>> cafdb1aede3476465c60235b7c6a7b009e43fa16



zalo_info = ZaloOAInfo(oa_id=OA_ID, secret_key=SECRET_KEY)
zalo_oa_client = ZaloOAClient(zalo_info)
class TextMessage(Mesage):
    """
    Class format text message
    """

    def convert_facebook(self, user_id: str = "", content: str = '', obj: list = None):
        """
        message send by format facebook
        :return:
        """
        data = json.dumps({
            "recipient": {
                "id": user_id
            },
            "message": {
                "text": content
            }
        })

        params = {
            "access_token": "{}".format(FACEBOOK_TOKEN_PAGE)
        }
        request = requests.post(FACEBOOK_API_ENDPOINT + "me/messages", params=params,
                                headers=self.headers, data=data)
        log_debug('############## %s ##############' % request.text)

    def convert_zalo(self, user_id: int = 0, content: str = '', obj: list = None):
        """
        message send by format zalo
        :return:

        """

        data = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": content
            }
        }

        params = {'data': data}
        zalo_oa_client.post('message', params)
        log_debug(str(user_id))
