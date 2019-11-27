# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:53:30 2019

@author: Lee
"""

import requests
import json
import time


class downloader(object):
    
    def __init__(self,aid,cid):
        """
        初始化函数
        
        """
        self.headers={    
             'Host': 'api.bilibili.com',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
             'Accept': '*/*',
             'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
             'Accept-Encoding': 'gzip, deflate, br',
             'Connection': 'keep-alive'
             }
        self.url='https://api.bilibili.com/x/web-interface/view?'
        self.aid=aid
        self.cid=cid

        
    def get_json_url(self):
        """
        获取CC字幕的json链接
        
        """
        params={
                'aid': self.aid,
                'cid': self.cid
                }
        r=requests.get(url=self.url,headers=self.headers,params=params)
        js=json.loads(r.text)
        self.title=js['data']['title']
        self.title=self.title.replace('/','').replace('\"','').replace('\/','').replace('>','').replace('<','').replace('?','').replace('*','').replace('\|','').replace(':','')
        subtitle=js['data']['subtitle']
        if subtitle['list']:
            json_url=subtitle['list'][0]['subtitle_url']
            return json_url
        else:
            print("该视频非CC字幕，无法抓取！")
            return ''
        
    def get_subtitles(self):
        """
        根据字幕的json 获取CC字幕
        
        """        
        json_url=self.get_json_url()
        if len(json_url)>0:
            with open('{}.srt'.format(self.title),'w',encoding='utf-8') as f:
                r=requests.get(json_url)
                info=json.loads(r.text)['body']
                for i in range(len(info)):
                    subtitle_from=info[i]['from']
                    subtitle_to=info[i]['to']
                    content=info[i]['content']
                    data=self.format_subtitle(subtitle_from,subtitle_to,content,i)
                    f.write(data)
            
        
       
    def format_subtitle(self,subtitle_from,subtitle_to,content,i):        
        """
        格式化成srt文件，形如：
        
        1
        00:00:01,035 --> 00:00:04,525
        远离了平行线 看吧天气预报也不怎么准
        
        """
        subtitle_from=round(subtitle_from,3)                                              #四舍五入为三位小数
        subtitle_to=round(subtitle_to,3)
        begin=time.strftime("%H:%M:%S",time.gmtime(subtitle_from))+','+self.rectify(subtitle_from)        
        end=time.strftime("%H:%M:%S",time.gmtime(subtitle_to))+','+self.rectify(subtitle_to)
        data=str(i+1)+'\n'+begin+' --> '+end+'\n'+content+'\n\n'                          #格式化成srt字幕
        return data
        

    def rectify(self,second):    
        """
        修正毫秒为三位
        """                   
        second=str(second).partition('.')[2]       #以.分割秒数
        if len(second)==0:
            second='000' 
        if len(second)==1:
            second+='00'
        if len(second)==2:
            second+='0'
        return second  

        

        
if __name__=='__main__':
    
    bilibili=downloader('55376285','96827743')
    bilibili.get_subtitles()
