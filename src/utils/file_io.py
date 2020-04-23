"""
read and write with file
"""
import io
import json

import pandas as pd


def read(filename, format_ex="txt", params=None):
    """
    Read file text
    :param filename: str
    :param params: data
    :param format_ex: str
    :return: str
    """
    if format_ex == "txt":
        with io.open(filename, "r", encoding="utf-8-sig") as file:
            text = file.read()
            return text
    elif format_ex == "json":
        with open(filename, 'r', encoding="utf-8-sig") as file:
            return json.load(file)
    elif format_ex == "csv":
        return pd.read_csv(filename,
                           error_bad_lines=False,
                           sep=params.get("sep"),
                           header=params.get("header"))
    return None


def write(filename, data, mode: str = "w", format_ex: str = "txt"):
    """
    Write context into file
    :param filename: str
    :param data: str or list
    :param mode: str
    :param format_ex: str
    :return:
    """
    if format_ex == "txt":
        with io.open(filename, "{}".format(mode), encoding="utf-8") as file:
            file.write(data)
    return None
