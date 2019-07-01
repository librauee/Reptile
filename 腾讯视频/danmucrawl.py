# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:02:15 2019

@author: Administrator
"""

import requests
import os
from pymongo import MongoClient


class Crawler(object):
    
    def __init__(self):
        """
        初始化函数
        """
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.'
                                      '38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                        }

        # 配置mongodb数据库
        host = os.environ.get('MONGODB_HOST', '127.0.0.1')  # 本地数据库
        port = os.environ.get('MONGODB_PORT', '27017')  # 数据库端口
        mongo_url = 'mongodb://{}:{}'.format(host, port)
        mongo_db = os.environ.get('MONGODB_DATABASE', 'TecentVedioDanmu')
        client = MongoClient(mongo_url)
        self.db = client[mongo_db]
        #self.db['TecentVedioDanmu'].create_index('id', unique=True)
        
    '''   
    def getHTMLText(self,url,headers):
        try:
            r=requests.get(url,headers=headers,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            return r.text
        except:
            return "爬取失败"
    '''
        
    def get_danmu(self):
        """
        爬取一集新版倚天屠龙记电视剧的弹幕
        """
        count=0
        target_list=[str(3748894695),str(3748894707),str(3748894703),str(3748894705),str(3748894704)]
        for target in target_list:
            url='http://mfm.video.qq.com/danmu?timestamp={}&target_id='+target
            page=1    
           
            for i in range(100):
                req_url=url.format(30*page)
                r=requests.get(req_url, headers=self.headers)
                for danmu in r.json(strict=False)['comments']:
                    self.parse_comment(danmu=danmu)               
                page+=1
            count+=1
            print("已将第{}集弹幕信息存入数据库".format(count))
            
        '''
        url = 'http://mfm.video.qq.com/danmu?timestamp={}&target_id=3748894707'        
        
        for i in range(100):
            req_url=url.format(30*page)
            r=requests.get(req_url, headers=self.headers)
            for danmu in r.json()['comments']:
                self.parse_comment(danmu=danmu)
            page+=1
        print("已将该集弹幕信息存入数据库")
        '''

    #695 707 703 705 704 696 706 702 3751228221 222 3753663998 999 3765083890 891 3767617669 668
                    
    def parse_comment(self, danmu):
        """
        解析函数，用来解析爬回来的json评论数据，并把数据保存进mongodb数据库
        """
        dmdic = {'content': danmu['content'], 'id': danmu['commentid'],
                 'upcount': danmu['upcount'],'timepoint': danmu['timepoint'],
                 'username': danmu['opername']
                   }  # 构造弹幕字典
        self.db['TecentVedioDanmu'].insert_one(dmdic)
    
if __name__=='__main__':
    dmcrawl=Crawler()
    dmcrawl.get_danmu()
    
    