# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 16:40:56 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json

#获取电影id
def get_movie_code(movie_name):
    if(movie_name==""):
        return
    url='http://maoyan.com/query?kw='+str(movie_name)
    proxy_pools={'ip': '120.234.138.101', '端口': '53779', '类型': 'HTTP', '位置': '广东省东莞市  移动', '响应速度': '2秒', '最后验证时间': '2019-02-07 14:31:02'}, {'ip': '180.164.24.165', '端口': '53281', '类型': 'HTTP', '位置': '上海市上海市  电信', '响应速度': '1秒', '最后验证时间': '2019-02-06 14:31:01'}, {'ip': '112.85.165.213', '端口': '9999', '类型': 'HTTP', '位置': '江苏省南通市  联通', '响应速度': '2秒', '最后验证时间': '2019-02-06 06:30:55'}, {'ip': '27.155.83.182', '端口': '8081', '类型': 'HTTP', '位置': '福建省福州市  电信', '响应速度': '3秒', '最后验证时间': '2019-02-05 18:31:01'}, {'ip': '111.177.161.82', '端口': '9999', '类型': 'HTTP', '位置': '湖北省随州市  电信', '响应速度': '3秒', '最后验证时间': '2019-02-03 20:31:01'}, {'ip': '222.135.92.68', '端口': '38094', '类型': 'HTTP', '位置': '山东省威海市  联通', '响应速度': '3秒', '最后验证时间': '2019-02-03 01:30:59'}, {'ip': '115.151.7.198', '端口': '9999', '类型': 'HTTP', '位置': '江西省宜春市  电信', '响应速度': '2秒', '最后验证时间': '2019-02-01 08:31:00'}, {'ip': '223.223.187.195', '端口': '80', '类型': 'HTTP', '位置': '中国 北京市 北京市 ', '响应速度': '1秒', '最后验证时间': '2019-01-31 18:31:01'}, {'ip': '117.95.198.249', '端口': '9999', '类型': 'HTTP', '位置': '江苏省宿迁市  电信', '响应速度': '2秒', '最后验证时间': '2019-01-30 13:31:01'}, {'ip': '219.134.90.116', '端口': '42931', '类型': 'HTTP', '位置': '广东省深圳市  电信', '响应速度': '3秒', '最后验证时间': '2019-01-29 07:31:01'}, {'ip': '117.114.149.10', '端口': '45801', '类型': 'HTTP', '位置': '北京市海淀区 BJENET宽带网络 BGP多线', '响应速度': '3秒', '最后验证时间': '2019-01-26 19:31:01'}
    proxy=random.choice(proxy_pools)
    proxy_ip = str(proxy['ip']) + ":" + str(proxy['端口'])
    proxies={
            'http':'http://'+proxy_ip,
            'https':'https://'+proxy_ip
            }

   
    print(proxy_ip)
    ua = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    responses=requests.get(url=url,headers=ua,proxies=proxies)
    print("请求代码:%d"%responses.status_code)
   
    html=BeautifulSoup(responses.text,"html.parser")
    #print(html)
    code=html.find('a',{'data-act':'movies-click','target':"_blank"})
    code=(code.attrs)['href'][7:]
    print(code)
    return code





# 解析每一页数据


def parse_one_page(html):

    data = json.loads(html)['cmts']  # 获取评论内容
    for item in data:
        yield{
            'date': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'comment': item['content']
        }

# 保存到文本文档中


def save_to_txt(movie_name):
    moviecode=get_movie_code(movie_name)
    proxy_pools={'ip': '120.234.138.101', '端口': '53779', '类型': 'HTTP', '位置': '广东省东莞市  移动', '响应速度': '2秒', '最后验证时间': '2019-02-07 14:31:02'}, {'ip': '180.164.24.165', '端口': '53281', '类型': 'HTTP', '位置': '上海市上海市  电信', '响应速度': '1秒', '最后验证时间': '2019-02-06 14:31:01'}, {'ip': '112.85.165.213', '端口': '9999', '类型': 'HTTP', '位置': '江苏省南通市  联通', '响应速度': '2秒', '最后验证时间': '2019-02-06 06:30:55'}, {'ip': '27.155.83.182', '端口': '8081', '类型': 'HTTP', '位置': '福建省福州市  电信', '响应速度': '3秒', '最后验证时间': '2019-02-05 18:31:01'}, {'ip': '111.177.161.82', '端口': '9999', '类型': 'HTTP', '位置': '湖北省随州市  电信', '响应速度': '3秒', '最后验证时间': '2019-02-03 20:31:01'}, {'ip': '222.135.92.68', '端口': '38094', '类型': 'HTTP', '位置': '山东省威海市  联通', '响应速度': '3秒', '最后验证时间': '2019-02-03 01:30:59'}, {'ip': '115.151.7.198', '端口': '9999', '类型': 'HTTP', '位置': '江西省宜春市  电信', '响应速度': '2秒', '最后验证时间': '2019-02-01 08:31:00'}, {'ip': '223.223.187.195', '端口': '80', '类型': 'HTTP', '位置': '中国 北京市 北京市 ', '响应速度': '1秒', '最后验证时间': '2019-01-31 18:31:01'}, {'ip': '117.95.198.249', '端口': '9999', '类型': 'HTTP', '位置': '江苏省宿迁市  电信', '响应速度': '2秒', '最后验证时间': '2019-01-30 13:31:01'}, {'ip': '219.134.90.116', '端口': '42931', '类型': 'HTTP', '位置': '广东省深圳市  电信', '响应速度': '3秒', '最后验证时间': '2019-01-29 07:31:01'}, {'ip': '117.114.149.10', '端口': '45801', '类型': 'HTTP', '位置': '北京市海淀区 BJENET宽带网络 BGP多线', '响应速度': '3秒', '最后验证时间': '2019-01-26 19:31:01'}
    proxy=random.choice(proxy_pools)
    proxy_ip = str(proxy['ip']) + ":" + str(proxy['端口'])
    proxies={
            'http':'http://'+proxy_ip,
            'https':'https://'+proxy_ip
            }   
    print(proxy_ip)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    
    for i in range(100,1000,5):
        try:
           
           originurl = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset=' + \
                 str(i)
           url=originurl.format(moviecode)
           
           r=requests.get(url,headers=headers,timeout=30,proxies=proxies)
           #r.raise_for_status()
           r.encoding=r.apparent_encoding
           print(r.status_code)
           html = r.text
           print("获取html，开始解析")
           print("开始保存第%d页" % i)
           for item in parse_one_page(html): 
              print(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','+ str(item['rate']) + ',' + item['comment'] + '\n')
              try:
                with open('movie_reviews2.txt', 'a', encoding='utf-8') as f:
                       f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ','
                        + str(item['rate']) + ',' + item['comment'] + '\n')
                #time.sleep(random.randint(1,100)/20)
                time.sleep(2)
              except Exception as e:
                f.close()
                continue
           #time.sleep(3)
        except Exception as e:
            continue

        f.close()
# 去重重复的评论内容


def delete_repeat(old, new):
    oldfile = open(old, 'r', encoding='utf-8')
    newfile = open(new, 'w', encoding='utf-8')
    content_list = oldfile.readlines()  # 获取所有评论数据集
    content_alread = []  # 存储去重后的评论数据集

    for line in content_list:
        if line not in content_alread:
            newfile.write(line + '\n')
            content_alread.append(line)
    print("去除重复评论完成")
            
def main():
    movie_name="流浪地球"
    save_to_txt(movie_name)
    delete_repeat(r'movie_reviews2.txt', r'movie_new.txt')
    
    
    #get_movie_code(movie_name)
    

if __name__ == '__main__':
    main()