# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:35:44 2019

@author: Lee
"""

import requests
import random
import time
from pymongo import MongoClient
from pandas.io.json import json_normalize

class yys(object):
    
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
        self.headers={
        'Referer': 'https://yys.cbg.163.com/cgi/mweb/pl/role?view_loc=all_list',
        'User-Agent': random.choice(self.user_agent)
                }
        self.url='https://recommd.yys.cbg.163.com/cgi-bin/recommend.py'
        self.db=MongoClient().cbg
        self.db2=MongoClient().proxy
        
        
    def get_proxy(self):
        mongo_proxy=self.db2.good_proxy
        proxy_data=mongo_proxy.find()
        proxy=json_normalize([ip for ip in proxy_data])
        proxy_list=list(proxy['ip'])
        return proxy_list
    

    def get_role_info(self):
        count=42
        proxy_list=self.get_proxy()
        while True:
            proxy=random.choice(proxy_list)
            params={
            #'callback': 'jQuery33108774469608762521_1565658137127',
            #'_': 1565658137128+count-1,
            'act': 'recommd_by_role',
            'search_type': 'role',
            'count': 15,
            'view_loc': 'all_list',
            'order_by': 'selling_time DESC',
            'page': count,
             }
            try:
                r=requests.get(self.url,headers=self.headers,params=params,proxies={'https': 'https://{}'.format(proxy),'http':'http://{}'.format(proxy)})
            
                for info in r.json()['result']:
                    allow_bargain=info['allow_bargain']
                    area_name=info['area_name']
                    desc_sumup_short=info['desc_sumup_short']
                    price=info['price']/100
                    server=info['server_name']
                    name=info['format_equip_name']
                    game_channel=info['game_channel']
                    expire_remain_seconds=info['expire_remain_seconds']
                    platform_type=info['platform_type']
                    level=info['level_desc']
                    collect_num=info['collect_num']

                    role={
                     'area_name':area_name,
                     'game_channel':game_channel,
                     'platform_type':platform_type,
                     'server':server,
                     'collect_num':collect_num,
                     'price':price,
                     'allow_bargain':allow_bargain,
                     'name':name,
                     'level':level,
                     'desc_sumup_short':desc_sumup_short,
                     'expire_remain_seconds':expire_remain_seconds
                     }
                    self.db['yys'].insert_one(role)
            
                print("已经存入第{}页角色信息".format(count))
                # time.sleep(5*random.random())
                count+=1
                if r.json()['paging']['is_last_page']:                
                    print("已经抓取到最后一页！")
                    break
            except:
                print("bad request!")
            
            
            
if __name__=='__main__':
    
    yys_crawl=yys()
    yys_crawl.get_role_info()