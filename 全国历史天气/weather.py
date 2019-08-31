# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 20:08:11 2019

@author: Administrator
"""

import requests
import threading
from pymongo import MongoClient
from lxml import etree


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
        province=tree.xpath('//ul[@class="clear"]/li/a/@href')[:34]
        return province
    
    def get_direct(self,directs,name):
        province=self.get_province()
        print(province)
        for pro in province:
            r=requests.get(self.origin_url+pro,headers=self.headers)
            tree=etree.HTML(r.text)
            direct_per_pro=tree.xpath('//ul[@class="clear"]/li/a/@href')
            name_per_pro=tree.xpath('//ul[@class="clear"]/li/a/text()')
            directs.extend(direct_per_pro)
            name.extend(name_per_pro)
    
    def get_weather(self,directs,name):
        direct_name=[]
        for direct in directs:
            direct_name.append(direct[7:-11])
        print(direct_name)
        for i in range(len(direct_name)):
            for year in range(2012,2019):
                for month in range(1,13):
                    if month<10:
                        r=requests.get(self.url.format(direct_name[i],year,'0'+str(month)),headers=self.headers)
                    else:
                        r=requests.get(self.url.format(direct_name[i],year,month),headers=self.headers)
                    tree=etree.HTML(r.text)
                    average_high_tem=tree.xpath('//h5[@class="red"]/text()')[0]
                    max_high_tem=tree.xpath('//h5[@class="red"]/text()')[1]
                    average_low_tem=tree.xpath('//tr/td[2]/h5/text()')[0]
                    min_low_tem=tree.xpath('//tr/td[2]/h5/text()')[1]
                    best_quality=tree.xpath('//td[@colspan="2"]/h5/text()')[0]
                    worst_quality=tree.xpath('//td[@colspan="2"]/h5/text()')[1]
                    item1={'average_high_tem':average_high_tem,
                           'max_high_tem':max_high_tem,
                           'average_low_tem':average_low_tem,
                           'min_low_tem':min_low_tem,
                           'best_quality':best_quality,
                           'worst_quality':worst_quality,
                           'city':name[i],
                           'year':year,
                           'month':month
                           }
                    self.db['info'].insert_one(item1)
    
    def main(self):
        self.get_province()
    
if __name__=='__main__':
    
    All_weather=weather()
    directs=[]
    name=[]
    All_weather.get_direct(directs,name)
    print(directs)
    All_weather.get_weather(directs,name)
