# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:45:25 2019

@author: Lee
"""

import requests
from lxml import etree
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import time

class weibo_night(object):
    
    def __init__(self,now):
        
        self.headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        self.base_url='https://huodong.weibo.com/netchina2019/'
        self.db=MongoClient().weibo
        self.now=now
        
    def people(self):
        
        r=requests.get(url=self.base_url+'people',headers=self.headers,params={'page':1})
        tree=etree.HTML(r.text)
        page=len(tree.xpath('//div[@class="night_pages"]/a/text()'))-1
        name=tree.xpath('//span[@class="txt"]/a/text()')
        num=tree.xpath('//span[@class="num"]/a/text() | //span[@class="num"]/text()')
        rank=tree.xpath('//span[@class="img_mark "]/em/text() | //span[@class="img_mark mark1"]/em/text() | //span[@class="img_mark mark2"]/em/text() | //span[@class="img_mark mark3"]/em/text()')
        num=[a[:-1].replace(",","") for a in num]
        for j in range(len(name)):
            item={
                  'name':name[j],
                  'num':num[j],
                  'rank':rank[j],
                  'time':self.now
                  }
            self.db['people'].insert_one(item)
            
        for i in range(2,page):
            params={'page':i}
            r=requests.get(url=self.base_url+'people',headers=self.headers,params=params)
            self.parse(r.text,db_name='people')
                
    def events(self):
        r=requests.get(url=self.base_url+'events',headers=self.headers)
        self.parse(r.text,db_name='events')
    
    def popular(self):
        
        r=requests.get(url=self.base_url+'popular',headers=self.headers)
        self.parse(r.text,db_name='popular')
        
    def parse(self,text,db_name):
        
        tree=etree.HTML(text)   
        name=tree.xpath('//span[@class="txt"]/a/text()')
        num=tree.xpath('//span[@class="num"]/a/text() | //span[@class="num"]/text()')
        rank=tree.xpath('//span[@class="img_mark "]/em/text() | //span[@class="img_mark mark1"]/em/text() | //span[@class="img_mark mark2"]/em/text() | //span[@class="img_mark mark3"]/em/text()')            
        num=[a[:-1].replace(",","") for a in num]
        for j in range(len(name)):
            item={
                  'name':name[j],
                  'num':num[j],
                  'rank':rank[j],
                  'time':self.now
                  }
            self.db['{}'.format(db_name)].insert_one(item)            

def main():
    
    now=int(time.time())    
    weibo=weibo_night(now)
    weibo.people()
    weibo.events()
    weibo.popular()    
    now=time.localtime(now)
    print(time.strftime("%Y-%m-%d %H:%M:%S",now))
    print("成功执行一次微博之夜数据监测！")
           
if __name__=='__main__':

    print("开启定时任务……")   
    scheduler=BlockingScheduler()
    scheduler.add_job(func=main,trigger='interval',minutes=30,misfire_grace_time=20)
    scheduler.start()