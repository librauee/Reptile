# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:09:28 2019

@author: Lee
"""
import datetime


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day*i


def get_date_list(start=None, end=None):
    """
    获取日期列表
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    if start is None:
        start = datetime.datetime.strptime("2018-01-01", "%Y-%m-%d")
    if end is None:
        end = datetime.datetime.strptime("2018-12-31", "%Y-%m-%d")
    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d.strftime("%Y-%m-%d"))
    return data

if __name__ == "__main__":
     print(get_date_list())
