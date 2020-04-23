"""
Interface message send to user
"""
try:
    from utils.logger import log_debug
except ImportError:
    from src.utils.logger import log_debug


class Mesage:
    """
    Interface message send to user
    """

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json"
        }

    def convert_facebook(self, recipient_id: str = "", content: str = "", obj: list = None):
        """
        message send by format facebook
        :return:
        """
        log_debug(recipient_id)

    def convert_zalo(self, recipient_id: str = "", content: str = "", obj: list = None):
        """
        message send by format facebook
        :return:
        """
        log_debug(recipient_id)
