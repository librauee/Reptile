# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:51:12 2019

@author: Lee
"""

from pymongo import MongoClient
from pandas.io.json import json_normalize
import pdfkit
import re
import time



# Mongo配置
conn=MongoClient('127.0.0.1', 27017)
db=conn.lol                    #连接lol数据库，没有则自动创建
mongo_lol=db.article           #使用article集合，没有则自动创建

# 配置wkhtmltopdf
config=pdfkit.configuration(wkhtmltopdf=r"F:\wkhtmltopdf\wkhtmltox-0.12.5-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe")
lol_url_data=mongo_lol.find()
data=json_normalize([article for article in lol_url_data])
url_list=list(data['article_url'])
title_list=list(data['title'])

# 修改title名，使之能够成为合法文件名
for i in range(len(title_list)):
    if title_list[i]:
        title_list[i]=re.sub('[\t\\\|\?\*\:\<\>\"\/]', '', title_list[i])

count=0
# url 转换成pdf存储
for url in url_list:    
    try:
        pdfkit.from_url(url, '{}.pdf'.format(title_list[count]),configuration=config)
        count+=1
        time.sleep(30)
    except:
        count+=1

print("已经将所有文章转换为PDF文件！")