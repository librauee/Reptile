# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:08:30 2019

@author: Lee
"""

import requests
from pymongo import MongoClient
import time
import random

class Typhoon(object):
    
    def __init__(self):
        self.user_agent=[
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
     # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25", 
    ]
        self.base_url='http://www.wztf121.com/data/complex/{}.json'
        self.headers={
                'Cookie': '_gscu_1378142123=65572018r5on4x80; _gscbrs_1378142123=1; vjuids=30469f88b.16c835d32ea.0.8062809782e9b; vjlast=1565572019.1565572019.30; Hm_lvt_e592d6befa4f9918e6496980d22c5649=1565572019; Wa_lvt_1=1565572019; Wa_lpvt_1=1565576034; _gscs_1378142123=65572018v2ofkf80|pv:8; Hm_lpvt_e592d6befa4f9918e6496980d22c5649=1565576061',
                'Host': 'www.wztf121.com',
                'Referer': 'http://www.wztf121.com/history.html',
                'User-Agent': random.choice(self.user_agent)
                }
        self.client=MongoClient()
        self.db=self.client.typhoon
        
        
    def get_year(self):
        
        year_list=[]
        years_url=self.base_url.format('years')
        r=requests.get(years_url,headers=self.headers)
        years=r.json()
        for year in years:
            year_list.append(year['year'])
        print("已获取所有有台风记录的年份！")
        return year_list
    
    def get_tf_list(self):
        
        tf_list=[]
        year_list=self.get_year()
        for year in year_list:
            url=self.base_url.format(year)
            r=requests.get(url,headers=self.headers)
            tfs=r.json()
            for tf in tfs:
                tfbh=tf['tfbh']
                tf_list.append(tfbh)
            time.sleep(random.random())
    
        print("已获取所有台风的编号，格式为‘年份+次序’")
        return tf_list
    
    
    def get_tf_detail(self):
        
        tf_list=self.get_tf_list()
        count=1
        for tf in tf_list:
            tf_url=self.base_url.format(tf)
            r=requests.get(tf_url,headers=self.headers)
            tf_detail=r.json()
            begin_time=tf_detail[0]['begin_time']
            ename=tf_detail[0]['ename']
            end_time=tf_detail[0]['end_time']
            name=tf_detail[0]['name']
            points=tf_detail[0]['points']
            for point in points:
                latitude=point['latitude']
                longitude=point['longitude']
                power=point['power']
                speed=point['speed']
                pressure=point['pressure']
                strong=point['strong']
                real_time=point['time']
                detail={
                        'name':name,
                        'ename':ename,
                        'latitude':latitude,
                        'longitude':longitude,
                        'power':power,
                        'speed':speed,
                        'pressure':pressure,
                        'strong':strong,
                        'time':real_time
                        }
                self.db['detail'].insert_one(detail)
            time.sleep(5*random.random())
            tf_info={
                    'name':name,
                    'ename':ename,
                    'begin_time':begin_time,
                    'end_time':end_time,
                    }
            
            self.db['info'].insert_one(tf_info)
            print("已存入第{}条台风详细信息！".format(count))
            count+=1
            
        
        
if __name__=='__main__':
    
    tfcraw=Typhoon()
    tfcraw.get_tf_detail()