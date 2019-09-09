# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 20:08:11 2019

@author: Administrator
"""

import requests
import threading
from pymongo import MongoClient
from lxml import etree
import time


class weather(object):

    def __init__(self):
        
        self.origin_url='https://m.tianqi.com'
        self.url='https://m.tianqi.com/lishi/{}/{}{}.html'
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        self.conn=MongoClient('127.0.0.1',27017)
        self.db=self.conn.weather
        
    def get_province(self):
        
        r=requests.get('https://m.tianqi.com/lishi.html',headers=self.headers)
        tree=etree.HTML(r.text)
        province_link=tree.xpath('//ul[@class="clear"]/li/a/@href')[:34]
        province=tree.xpath('//li/a/text()')[:34]
        return province_link,province
    
    def get_direct(self,directs,name):
        
        province_link,province=self.get_province()
        print(province)
        for pro in province_link:
            r=requests.get(self.origin_url+pro,headers=self.headers)
            tree=etree.HTML(r.text)
            direct_per_pro=tree.xpath('//ul[@class="clear"]/li/a/@href')
            name_per_pro=tree.xpath('//ul[@class="clear"]/li/a/text()')
            directs.append(direct_per_pro)
            name.append(name_per_pro)
            
        return province
    
    def get_weather(self,directs,name,province):
        
#        direct_name=[]
#        for i in range(len(province)):
#            for direct in directs[i]:
#                direct_name.append(direct[7:-11])
#        print(direct_name)
        for i in range(len(province)):
            for j in range(len(directs[i])):
                
                for year in range(2012,2019):
                    tasks=[]
                    for month in range(1,13):
                        task=threading.Thread(target=self.run, args=(i,j,year,month,directs[i][j][7:-11],province[i]))
                        tasks.append(task)
                        task.start()
                    # 等待所有线程完成
                    for _ in tasks:
                        _.join()
                    
    
    def run(self,i,j,year,month,direct_name,province_name):
        
        try:
            if month<10:
                r=requests.get(self.url.format(direct_name,year,'0'+str(month)),headers=self.headers)
            else:
                r=requests.get(self.url.format(direct_name,year,month),headers=self.headers)
            tree=etree.HTML(r.text)
            average_high_tem=tree.xpath('//h5[@class="red"]/text()')[0]
            max_high_tem=tree.xpath('//h5[@class="red"]/text()')[1]
            average_low_tem=tree.xpath('//tr/td[2]/h5/text()')[0]
            min_low_tem=tree.xpath('//tr/td[2]/h5/text()')[1]
            best_quality=tree.xpath('//td[@colspan="2"]/h5/text()')[0]
            worst_quality=tree.xpath('//td[@colspan="2"]/h5/text()')[1]
            date=tree.xpath('//dd[@class="date"]/text()')
            weather=tree.xpath('//dd[@class="txt1"]/text()')
            date=[d[:5] for d in date]
            dic=dict(zip(date,weather))
            item1={
               'average_high_tem':average_high_tem,
               'max_high_tem':max_high_tem,
               'average_low_tem':average_low_tem,
               'min_low_tem':min_low_tem,
               'best_quality':best_quality,
               'worst_quality':worst_quality,
               'city':name[i][j],
               'year':year,
               'month':month,
               'weather':dic,
               'province':province_name
                           }
            self.db['info'].insert_one(item1)
        except Exception as e:
            print(e)
            #time.sleep(2)
            #self.run(i,j,year,month,direct_name,province_name)
        
    
if __name__=='__main__':
    
    All_weather=weather()
    directs=[]
    name=[]
    province=All_weather.get_direct(directs,name)
    print(directs)
    All_weather.get_weather(directs,name,province)

