# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:20:17 2019

@author: Administrator
"""

import requests

from bs4 import BeautifulSoup

def getHTMLText(url,headers):
    try:
        r=requests.get(url,headers=headers,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "爬取失败"


def parsehtml(html):
   soup = BeautifulSoup(html,'html.parser')
   all_topics=soup.find_all('tr')[5:]
   for each_topic in all_topics:
       times = each_topic.find('td', class_='last')  # 搜索指数
       rank = each_topic.find('td', class_='first')  # 排名
       name = each_topic.find('a', class_='list-title')  # 标题目
       #去除其他的td标签的内容，并获取文本，进行输出格式校对
       if rank != None and name != None and times != None:
           rank = each_topic.find('td', class_='first').get_text().replace(' ', '').replace('\n', '')
           name = each_topic.find('a', class_='list-title').get_text().replace(' ', '').replace('\n', '')
           times = each_topic.find('td', class_='last').get_text().replace(' ', '').replace('\n', '')
           tplt = "排名：{0:^4}\t标题：{1:{3}^15}\t搜索指数：{2:^8}"
           print(tplt.format(rank, name, times, chr(12288)))

def main():
    #百度实时热点排行榜单链接
    url = 'http://top.baidu.com/buzz?b=1&fr=topindex'
    headers = {'User-Agent': 'MMozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    html = getHTMLText(url, headers)
    parsehtml(html)

if __name__ == '__main__':
    main()
