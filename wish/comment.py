# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:35:38 2019

@author: Lee
"""

import requests
import json
from pymongo import MongoClient
import random
import time
import pandas as pd



class goods_comment(object):
    
    def __init__(self):
        
        self.url='https://www.wish.com/api/product-ratings/get'
        self.headers={
            'cookie': '',
            'origin': 'https://www.wish.com',
            # 'referer': 'https://www.wish.com/product-ratings/5b8649728fd66028f6822882',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-xsrftoken': '2|14b9ee6c|86b9486b92004136183f0675fb41c5d5|1570535069',
            }
        self.db=MongoClient().wish
        
    def get_comment(self,product_id):
        
        data={
            'product_id': product_id,
            'start': 0,
            'count': 30,
            #'request_count': 3,
                
                }
        
        r=requests.post(self.url,data=data,headers=self.headers)
        goods_data=r.json()['data']
        next_offset=goods_data['next_offset']
        num_results=goods_data['num_results']
        results=goods_data['results']
        
        for result in results:
            comment=result['comment']
            rating=result['rating']
            comment_time=result['time']
            size_choice=result['size_choice']
            user=result['user']
            user_downvoted=result['user_downvoted']
            user_upvoted=result['user_upvoted']
            
            item={
                  'product_id':product_id,
                  'comment':comment,
                  'rating':rating,
                  'comment_time':comment_time,
                  'size_choice':size_choice,
                  'user':user,
                  'user_downvoted':user_downvoted,
                  'user_upvoted':user_upvoted,
                    }
            self.db['comment'].insert_one(item)
            
        while next_offset<num_results:
            data={
            'product_id': product_id,
            'start': next_offset,
            'count': 30,
            #'request_count': 3,               
                }     
            r=requests.post(self.url,data=data,headers=self.headers)
            goods_data=r.json()['data']
            next_offset=goods_data['next_offset']
            results=goods_data['results']
            for result in results:
                
                comment=result['comment']
                rating=result['rating']
                comment_time=result['time']
                size_choice=result['size_choice']
                user=result['user']
                user_downvoted=result['user_downvoted']
                user_upvoted=result['user_upvoted']
            
                item={
                  'product_id':product_id,
                  'comment':comment,
                  'rating':rating,
                  'comment_time':comment_time,
                  'size_choice':size_choice,
                  'user':user,
                  'user_downvoted':user_downvoted,
                  'user_upvoted':user_upvoted,
                    }
                self.db['comment1'].insert_one(item)

def get_list():
    
    df=pd.read_excel('G1.xlsx')
    data=list(df['Product URL'])
    data=[i[23:] for i in data]
    return data
          
            
            
if __name__=='__main__':

    product_id_list=get_list()

    a=goods_comment()
    for product_id in product_id_list:
        a.get_comment(product_id)
        print("已经成功爬取ID为{}的商品评论信息!".format(product_id))
        time.sleep(random.random()*3)


