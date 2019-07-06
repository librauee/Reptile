# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:51:10 2019

@author: Lee
"""
from pymongo import MongoClient
from pandas.io.json import json_normalize
import pdfkit
import re



# Mongo配置
conn=MongoClient('127.0.0.1', 27017)
db=conn.wx                    #连接wx数据库，没有则自动创建
mongo_wx=db.article           #使用article集合，没有则自动创建

# 配置wkhtmltopdf
config=pdfkit.configuration(wkhtmltopdf=r"F:\wkhtmltopdf\wkhtmltox-0.12.5-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe")
wx_url_data=mongo_wx.find()
data=json_normalize([comment for comment in wx_url_data])
url_list=list(data['content_url'])
title_list=list(data['title'])
# 修改title名，使之能够成为文件名
for i in range(len(title_list)):
    if title_list[i]:
        title_list[i]=re.sub('[\t\\\|\?\*\:\<\>\"\/]', '', title_list[i])
count=0
# url 转换成pdf存储
for url in url_list:    
    if url:
        pdfkit.from_url(url, '{}.pdf'.format(title_list[count]),configuration=config)
    count+=1
print("已经将所有文章转换为PDF文件！")
        


