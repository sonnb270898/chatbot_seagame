"""
Model route chatbot
"""
try:
    from nlp.nlp_predict import NLPPredictor
    from utils.logger import log_info
    from utils.utils import get_response_random, check_exists_create
    from response.query import get_ranking, get_athlete, get_result, get_schedule
    from response.string import *
    from response.generation_reply import Response
except ImportError:
    # for develop
    from src.response.generation_reply import Response
    from src.utils.logger import log_info
    from src.nlp.nlp_predict import NLPPredictor
    from src.response.query import get_ranking, get_athlete, get_result, get_schedule
    from src.response.string import *
    from src.utils.utils import get_response_random, check_exists_create


class Dialog:
    """
    Model route chatbot
    """

    def __init__(self):
        self.nlp = NLPPredictor()
        self.response = Response()

    def __handle_response(self, message, data, type_reply, user_id, source):
        """
        handle response
        :param message: str
        :param data: list
        :param type_reply: str
        :param recipient_id: str
        :return:
        """
        log_info('######## HANDLE RESPONSE FOR USER [{}] ########'.format(user_id))

        if type_reply == "text":
            self.response.response_text(user_id=user_id, content=message[:2000], obj=data,
                                        source=source)
        elif type_reply == "quick_replies":
            self.response.response_quick_reply(user_id=user_id, content=message[:2000],
                                               obj=data, source=source)

    def handle_message(self, user_id=0, input_text="", page_id=0, source=""):
        """
        Handle input is text of user
        :param recipient_id: int
        :param input_text: str
        :param page_id: int
        :param source: str
        """

        data = list()
        log_info(
            '######## USER [{} - {}] SEND NEW MESSAGE ########'.format(user_id, page_id))
        check_exists_create(fb_id=user_id, page_id=page_id)
        snips = self.nlp.get_snips(input_text)
        if source == 'facebook':
            if snips.get("intent") == 'define':
                message = get_response_random(STR_DEFINE)
                type_reply = "quick_replies"
                data = [{
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
                }]
            elif snips.get("intent") == 'host':
                message = get_response_random(STR_HOST)
                type_reply = "text"
            elif snips.get("intent") == 'list_sports':
                message = get_response_random(STR_LST_SPORTS)
                type_reply = "text"
            elif snips.get("intent") == 'list_countries':
                message = get_response_random(STR_LST_NUMBER_CONTRIES)
                type_reply = "text"
            elif snips.get("intent") == 'mascot':
                message = get_response_random(STR_MASCOT)
                type_reply = "text"
            elif snips.get("intent") == 'rank':
                message = get_ranking()
                type_reply = "text"
            elif snips.get("intent") == 'athele':
                message = get_athlete(snips.get("entity").get("is_name")[0])
                data = [
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
                type_reply = "quick_replies"
            elif snips.get("intent") == 'schedule':
                data = [
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
                message = get_schedule(snips.get("entity").get("date_start"),
                                       snips.get("entity").get("date_stop"),
                                       snips.get("entity"))
                type_reply = "quick_replies"
            elif snips.get("intent") == 'result':
                data = [
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
                message = get_result(snips.get("entity").get("date_start"),
                                     snips.get("entity").get("date_stop"), snips.get("entity"))
                type_reply = "quick_replies"
            else:
                type_reply = "text"
                message = "Mời bạn nhập lại câu hỏi"
        if source == 'zalo':
            if snips.get("intent") == 'define':
                message = get_response_random(STR_DEFINE)
                type_reply = "quick_replies"
            elif snips.get("intent") == 'host':
                message = get_response_random(STR_HOST)
                type_reply = "text"
            elif snips.get("intent") == 'list_sports':
                message = get_response_random(STR_LST_SPORTS)
                type_reply = "text"
            elif snips.get("intent") == 'list_countries':
                message = get_response_random(STR_LST_NUMBER_CONTRIES)
                type_reply = "text"
            elif snips.get("intent") == 'mascot':
                message = get_response_random(STR_MASCOT)
                type_reply = "text"
            elif snips.get("intent") == 'rank':
                message = get_ranking()
                type_reply = "text"
            elif snips.get("intent") == 'athele':
                data = [
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
                message = get_athlete(snips.get("entity").get("is_name")[0])
                type_reply = "quick_replies"
            elif snips.get("intent") == 'schedule':
                data = [
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
                message = get_schedule(snips.get("entity").get("date_start"),
                                       snips.get("entity").get("date_stop"),
                                       snips.get("entity"))
                type_reply = "quick_replies"
            elif snips.get("intent") == 'result':
                data = [
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
                message = get_result(snips.get("entity").get("date_start"),
                                     snips.get("entity").get("date_stop"), snips.get("entity"))
                type_reply = "quick_replies"
            else:
                type_reply = "text"
                message = "Mời bạn nhập lại câu hỏi"


        self.__handle_response(message, data, type_reply, user_id, source)
