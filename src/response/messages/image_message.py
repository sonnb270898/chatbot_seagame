"""
Class format image message
"""
import json
import requests
from dialog.models.api.messages.message import Mesage
from utils.logger import log_debug
from utils.settings import FACEBOOK_API_ENDPOINT


class ImageMessage(Mesage):
    """
    Class format image message
    """

    def convert_facebook(self, recipient_id: str = "", content: str = '', obj: list = None):
        """
        message send by format facebook
        :return:
        """
        page_id = recipient_id.split("_")[1]
        fb_id = recipient_id.split("_")[0]
        data = json.dumps({
            "recipient": {
                "id": fb_id
            },
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": content,
                        "is_reusable": True
                    }
                }
            }
        })
        pages = self.connect.get("pages")
        if pages:
            pages = json.loads(pages)
            access_token = [_.get("page_token") for _ in pages if
                            str(_.get("page_id")) == page_id][0]
            params = {
                "access_token": "{}".format(access_token)
            }
            request = requests.post(FACEBOOK_API_ENDPOINT + "me/messages", params=params,
                                    headers=self.headers,
                                    data=data)
            log_debug('############## %s ##############' % request.text)
        else:
            log_debug("############## Can't get pages ##############")

    def convert_zalo(self, recipient_id: int = 0, content: str = '', obj: list = None):
        """
        message send by format facebook
        :return:
        """
        log_debug(recipient_id)
