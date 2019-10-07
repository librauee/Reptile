# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 21:21:25 2019

@author: Administrator
"""

import requests
from lxml import etree
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import time

class Hot(object):
    
    def __init__(self):
        
        self.url_zhihu='https://www.zhihu.com/hot'
        self.headers_zhihu={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'cookie': ''
            }
        self.url_weibo='https://s.weibo.com/top/summary?cate=realtimehot'
        self.headers_weibo={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            }
        self.db=MongoClient().hot

        
        
    def zhihu_crawl(self):
        
        source='zhihu'
        r=requests.get(self.url_zhihu,headers=self.headers_zhihu)
        tree=etree.HTML(r.text)
        link=tree.xpath('//div[@class="HotItem-content"]/a/@href')
        title=tree.xpath('//div[@class="HotItem-content"]/a/h2[@class="HotItem-title"]/text()')
        return link,title,source
    
    
    def weibo_crawl(self):
        
        source='weibo'
        r=requests.get(self.url_weibo,headers=self.headers_weibo)
        tree=etree.HTML(r.text)
        link=tree.xpath('//td[@class="td-02"]/a/@href')
        title=tree.xpath('//td[@class="td-02"]/a/text()')
        link=['https://s.weibo.com'+i for i in link]
        return link,title,source
    
    def get_item(self,link,title,source):
        
        self.db['{}'.format(source)].delete_many({})
        items=[]
        for i in range(len(link)):
            item={
              'title':title[i],
              'link':link[i]
            }
            items.append(item)
        self.db['{}'.format(source)].insert_many(items)


def main():
    
    now=time.time()
    now=time.localtime(now)
    now=time.strftime("%Y-%m-%d %H:%M:%S",now)
    hot=Hot()
    link,title,source=hot.zhihu_crawl()
    hot.get_item(link,title,source)
    link,title,source=hot.weibo_crawl()
    hot.get_item(link,title,source)
    print("微博，知乎热榜已更新至{}".format(now))     

def run():
    
    print("开启定时任务……")
    scheduler=BlockingScheduler()
    scheduler.add_job(func=main,trigger='interval',minutes=20)
    scheduler.start()
            
            
if __name__=='__main__':
    
    run()
    
