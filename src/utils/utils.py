"""
Generation random sentence to answer for user
"""
import random

try:
    from utils.mysql_connection import Connection, MySQLError
    from utils.logger import log_debug, log_error
except ImportError:
    from src.utils.mysql_connection import Connection, MySQLError
    from src.utils.logger import log_debug, log_error


def get_response_random(reply: list):
    """
    get random sentence in list sentences
    :param reply: list
    :return:
    """
    if reply:
        index = random.randint(0, len(reply) - 1)
        return reply[index]
    return ""


def check_exists_create(fb_id, page_id):
    """
    Check user is exists, if not create new one
    :param fb_id: str
    :param page_id: str
    :return:
    """
    connection = Connection().get_connection()
    try:
        cursor = connection.cursor()  # prepare an object cursor
        query = """
                SELECT * FROM follower WHERE fb_id={};
                """.format(fb_id)
        log_debug(query)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            query = """
                    INSERT INTO follower (fb_id, page_id)
                    VALUES ('{}', '{}');
                    """.format(fb_id, page_id)
            log_debug(query)
            cursor.execute(query)
            cursor.close()
            del cursor
            connection.commit()
        # connection.close()
    except MySQLError as ex:
        # connection.close()
        log_error("Can't check exists then create one: {}".format(ex))
