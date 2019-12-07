# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 09:50:50 2019

@author: Administrator
"""

import requests
import re
import time
import random
from redis import Redis


#girl 34243513, 266808424, 50426133, 267707433, 20627581, 35584492
#boy 20300634, 67030741, 48141169, 270953449
class Zhihu(object):
    
    def __init__(self):
        
        self.url='https://www.zhihu.com/api/v4/questions/35584492/answers'
        self.headers={
                'cookie': '',
                'referer': 'https://www.zhihu.com/question/35584492',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
        self.r=Redis.from_url("redis://127.0.0.1:6379?db=10", decode_responses=True)
        
    def get_urls(self,offset,urls):
        
        params={
                'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
                'limit': 5,
                'offset': offset,
                'platform': 'desktop',
                'sort_by': 'default'              
                }
        r=requests.get(self.url,headers=self.headers,params=params)
        data=r.json()['data']
        for i in data:
            content=i['content']
            pic_urls=re.findall(r'data-actualsrc="(.*?.(gif|jpg|png))',content)
            for j in range(len(pic_urls)):
                self.r.sadd("urls",pic_urls[j][0])                

    
    
    def get_total(self):
                
        params={
                'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
                'limit': 5,
                'offset': 0,
                'platform': 'desktop',
                'sort_by': 'default'              
                }
        r=requests.get(self.url,headers=self.headers,params=params)
        totals=r.json()['paging']['totals']              
        return totals
        
          
    
if __name__=='__main__':
    
    crawl=Zhihu()
    total=crawl.get_total()
    page=int(total/5)+1
    urls=[]
    for i in range(100):
        crawl.get_urls(offset=i*5,urls=urls)
        print("已抓取第{}页回答的全部图片链接！".format(i+1))
        time.sleep(random.random())