import json
import time

import requests

from zalo.sdk import APIConfig
from zalo.sdk.APIException import APIException
from zalo.sdk.ZaloBaseClient import ZaloBaseClient
from zalo.sdk.utils.MacUtils import MacUtils
from src.config import API_OA_LINK,ZALO_TOKEN

class ZaloOAInfo:
    def __init__(self, oa_id, secret_key):
        self.oa_id = oa_id
        self.secret_key = secret_key


class ZaloOAClient(ZaloBaseClient):
    def __init__(self, oa_info):
        self.oa_info = oa_info

    def post(self, url, data):
        endpoint = "%s/%s%s" % (API_OA_LINK, url, ZALO_TOKEN)
        params = self.create_oa_params(data, self.oa_info)
        return self.send_request(endpoint, params, 'POST')

