# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 19:25:18 2019

@author: Lee
"""
import requests
from pymongo import MongoClient



# Mongo配置
conn=MongoClient('127.0.0.1', 27017)
db=conn.lol                    #连接lol数据库，没有则自动创建
mongo_lol=db.article           #使用article集合，没有则自动创建
headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
url='http://qt.qq.com/lua/lol_news/recommend_refresh?cid=12&plat=ios'
r=requests.get(url,headers=headers).json()
datalist=[]
update_list=r['update_list']

for update in update_list:
    
    article_url=update['article_url']
    image_url=update['image_url_big']
    publication_date=update['publication_date']
    title=update['title']
    author=update['author']
    
    data={'article_url':article_url,
          'image_url':image_url,
          'publication_date':publication_date,
          'title':title,
          'author':author            
            }
    mongo_lol.insert_one(data)
print("掌盟文章数据已经完全入库！")

'''
import urllib.request
urllib.request.urlretrieve(url,'name.html')
'''
    



    