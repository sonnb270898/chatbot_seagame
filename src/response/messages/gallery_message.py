"""
Class format gallery message
"""
import json
import requests
from dialog.models.api.messages.message import Mesage
from utils.logger import log_debug
from utils.settings import FACEBOOK_API_ENDPOINT
from utils.reply.post_back import PRODUCT

WEB_URL = "https://canifa.com/"
IMAGE_URL = "https://canifa.s3.amazonaws.com/media/catalog/product/" \
            "cache_generated/235x310/6ta18s002-sk010-33.jpg"
TITLE = "QUAN TÂM"


class GalleryMessage(Mesage):
    """
    Class format gallery message
    """

    def convert_facebook(self, recipient_id: str = "", content: str = "", obj: list = None):
        """
        message send by format facebook
        :return:
        """
        page_id = recipient_id.split("_")[1]
        fb_id = recipient_id.split("_")[0]

        list_product = []
        for item in obj:
            product = {
                "title": "%s" % item.get("title"),
                "image_url": "%s" % item.get("image_url") if item.get(
                    "image_url") is not None else IMAGE_URL,
                "default_action": {
                    "type": "web_url",
                    "url": "%s" % item.get("product_url") if item.get(
                        "product_url") is not None else WEB_URL,
                    "webview_height_ratio": "tall",
                },
            }
            if content != "default":
                product.update(
                    {
                        "buttons": [
                            {
                                "type": "postback",
                                "title": TITLE,
                                "payload": PRODUCT + "_%s" % item.get("id")
                            }
                        ]
                    }
                )
            list_product.append(product)
        list_product = list_product[:10]
        data = json.dumps({
            "recipient": {
                "id": fb_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": list_product
                    }
                }
            }
        })
        print(data)

        pages = self.connect.get("pages")
        if pages:
            pages = json.loads(pages)
            access_token = [_.get("page_token") for _ in pages if
                            str(_.get("page_id")) == page_id][0]
            params = {
                "access_token": "{}".format(access_token)
            }
            request = requests.post(FACEBOOK_API_ENDPOINT + "me/messages", params=params,
                                    headers=self.headers, data=data)
            log_debug("############## %s ##############" % request.text)
        else:
            log_debug("############## Can't get pages ##############")

    def convert_zalo(self, recipient_id: str = "", content: str = "", obj: list = None):
        """
        message send by format facebook
        :return:
        """
        log_debug(recipient_id)
