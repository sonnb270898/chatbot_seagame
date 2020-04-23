"""
Response Facebook
"""
try:
    from response.messages.text_message import TextMessage
    from response.messages.quick_reply_message import QuickReplyMessage
except ImportError:
    from src.response.messages.text_message import TextMessage
    from src.response.messages.quick_reply_message import QuickReplyMessage


class Response:
    """
    Response Facebook
    """

    def __init__(self):
        self.text = TextMessage()
        # self.image = ImageMessage()
        # self.gallery = GalleryMessage()
        # self.button = ButtonMessage()
        self.quick_reply = QuickReplyMessage()

    def response_text(self, user_id: str, content: str, obj: list, source: str):
        """
        response text
        :param fb_id: str
        :param content: str
        :param obj: list
        :param source: str
        :return:
        """
        if source == "facebook":
            self.text.convert_facebook(user_id=user_id, content=content, obj=obj)
        if source == "zalo":
            self.text.convert_zalo(user_id=user_id, content=content, obj=obj)

    def response_image(self, user_id: str, content: str, obj: list):
        """
        response image
        :param fb_id: str
        :param content: str
        :param obj: list
        :return:
        """
        self.image.convert_facebook(user_id=user_id, content=content, obj=obj)

    def response_button(self, user_id: str, content: str, obj: list):
        """
        response button
        :param fb_id: str
        :param content: str
        :param obj: list
        :return:
        """

        self.button.convert_facebook(user_id=user_id, content=content, obj=obj)

    def response_gallery(self, user_id: str, content: str, obj: list):
        """
        response gallery
        :param fb_id: str
        :param content: str
        :param obj: list
        :return:
        """
        self.gallery.convert_facebook(user_id=user_id, content=content, obj=obj)

    def response_quick_reply(self, user_id: str, content: str, obj: list, source: str):
        """
        response quick reply
        :param fb_id: str
        :param content: str
        :param obj: list
        :param source: list
        :return:
        """
        if source == "facebook":
            self.quick_reply.convert_facebook(user_id=user_id, content=content, obj=obj)
        if source == "zalo":
            self.quick_reply.convert_zalo(user_id=user_id,content=content, obj=obj)
