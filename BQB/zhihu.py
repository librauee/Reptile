# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 10:33:55 2019

@author: Administrator
"""


import requests
import re
import time
import random

class Zhihu(object):
    
    def __init__(self):
        
        self.url='https://www.zhihu.com/api/v4/questions/310564833/answers'
        self.headers={
                'cookie': '',
                'referer': 'https://www.zhihu.com/question/310564833',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
        
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
                urls.append(pic_urls[j][0])                

    
    
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
        
       
    def download(self,urls):
        
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        for i in range(len(urls)):
            r=requests.get(urls[i],headers=headers)
            with open('{}{}'.format(i+1,urls[i][-4:]),'wb') as f:
                 f.write(r.content)
    
if __name__=='__main__':
    
    crawl=Zhihu()
    total=crawl.get_total()
    page=int(total/5)+1
    urls=[]
    for i in range(page):
        crawl.get_urls(offset=i*5,urls=urls)
        print("已抓取第{}页回答的全部表情包链接！".format(i+1))
        time.sleep(random.random())
    crawl.download(urls)