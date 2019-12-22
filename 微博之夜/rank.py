# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 12:12:39 2019

@author: Lee
"""

from pymongo import MongoClient
import pandas as pd
import time


def timestamp(t):
    t=time.localtime(t)
    return time.strftime("%Y-%m-%d %H:%M:%S",t)
    

db=MongoClient().weibo
#data=pd.DataFrame(list(db['events'].find()))
#data=data.drop(['_id','rank'],axis=1)
#data['time']=data['time'].apply(timestamp)
#data['type']='Events'
#data.columns=['name','value','date','type']
#print(data)
#data.to_csv('events.csv', index=None,encoding='utf_8_sig')

#data2=pd.DataFrame(list(db['people'].find()))
#data2=data2.drop(['_id','rank'],axis=1)
#data2['time']=data2['time'].apply(timestamp)
#data2['type']='People'
#data2.columns=['name','value','date','type']
#data2.to_csv('people.csv', index=None,encoding='utf_8_sig')

data3=pd.DataFrame(list(db['popular'].find()))
data3=data3.drop(['_id','rank'],axis=1)
data3['time']=data3['time'].apply(timestamp)
data3['type']='Popular'
data3.columns=['name','value','date','type']
data3.to_csv('popular.csv', index=None,encoding='utf_8_sig')