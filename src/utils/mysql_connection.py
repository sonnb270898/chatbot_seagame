"""Class config connect with mysql"""
import sys

import pymysql.cursors
from pymysql import MySQLError

try:
    from utils.singleton import Singleton
    from config import MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER
except ImportError:
    from src.utils.singleton import Singleton
    from src.config import MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER


class Connection(metaclass=Singleton):
    """Class config connect with mysql"""

    def __init__(self):
        try:
            self.connect = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                db=MYSQL_DATABASE,
                use_unicode=True,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
        except MySQLError as ex:
            sys.exit("Can't get into the database %s" % ex)

    def get_connection(self):
        """
        Get connection
        """
        return self.connect

    def close_connecttion(self):
        """
        Delete connection
        """
        del self.connect
        Connection.delete_instance()
