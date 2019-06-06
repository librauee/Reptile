# -*- coding: utf-8 -*-

import requests
import time

_type_ = "US"                                        #香港就填Hk

headers={
         "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
         "Cookie": "",                               #上雪球把自己的cookie复制下来
         }

f = open("xueqiu.csv", "w")
f.write("symbol, name, current, percent, market_capital, pe_ttm\n")


def get_json(page):                                  #带上cookie get请求
    return requests.get("https://xueqiu.com/service/v5/stock/screener/quote/list?page={}"
                        "&size=30&order=desc&orderby=percent&order_by=percent&market={}"
                        "&type={}&_={}".format(page, _type_, _type_, int(time.time()*1000)),
                        headers=headers).json()


def parse_json(data, _all):                          #解析数据
    _list = data["data"]["list"]
    for _each in _list:
        symbol = _each.get("symbol")                 #股票代码
        name = _each.get("name")                     #股票名称
        current = _each.get("current")               #当前价格
        percent = _each.get("percent")               #涨跌幅
        market_capital = _each.get("market_capital") #市值
        pe_ttm = _each.get("pe_ttm")                 #市盈率
        f.write(','.join(map(str, [symbol,name,current,percent,market_capital,pe_ttm])))
        f.write("\n")
        _all += 1
        if _all == 100:
            break
    return _all


def main():
    _all = 0
    for i in range(1,5):
        data = get_json(i)
        _all = parse_json(data, _all)

        time.sleep(5)                                #sleep 5s，


def test():
    print(requests.get("https://xueqiu.com/service/v5/stock/screener/quote/list?page=3&size=30&order=desc&orderby=percent&order_by=percent&market=US&type=us&_=1555485032232",
                       headers=headers).json())

if __name__ == "__main__":

    main()
    # test()
