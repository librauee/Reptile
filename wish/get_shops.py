# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:54:01 2019

@author: Lee
"""

import requests
import json
from pymongo import MongoClient
from pandas.io.json import json_normalize
import time
import random

def getproxy():
    
    conn=MongoClient('127.0.0.1', 27017)
    db=conn.proxy
    mongo_proxy=db.good_proxy
    proxy_data=mongo_proxy.find()
    proxy=json_normalize([ip for ip in proxy_data])
    proxy_list=list(proxy['ip'])
    return proxy_list




class shop(object):
    
    def __init__(self):
        
        self.url='http://www.haiyingshuju.com/wish_2.0/merchant/list'
        self.headers={
             'Cookie': 'today=8; Hm_lvt_03a80b70183e649c063d5ee13290d51b=1570535053; Hm_lpvt_03a80b70183e649c063d5ee13290d51b=1570535053',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',             
             'Host': 'www.haiyingshuju.com',
             'Origin': 'http://www.haiyingshuju.com',
             'token':'', 
             'Referer':'http://www.haiyingshuju.com/wish/index.html',
             'Content-Type': 'application/json;charset=UTF-8',
             'Accept': 'application/json, text/plain, */*',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
             'Connection': 'keep-alive',
             'Content-Length': '416'

             }
        self.db=MongoClient().wish
    
    def get_list(self):
        
        # proxy=getproxy()
        # 2014-2018
        for year in range(2014,2019):
            for month in range(1,13):
                if month<10:
                    data={
                        'approvedDateStart': "{}-0{}-01".format(year,month),
                        'approvedDateEnd': "{}-0{}-01".format(year,month+1),
                        'hot60CountEnd': "",
                        'hot60CountStart': "",
                        'index': 1,
                        'intervalRatingSumEnd': "",
                        'intervalRatingSumStart': "",
                        'merchant': "",
                        'merchantOrMname': "",
                        'mname': "",
                        'numEnteredEnd': "",
                        'numEnteredStart': "",
                        'numRatingEnd': "",
                        'numRatingStart': "",
                        'orderColumn': "view_rate_sum",
                        'pageSize': 50,
                        'ratingEnd': "",
                        'ratingStart': "",
                        'sort': "DESC",
                        'token': "",
                        'viewRateSumEnd': "",
                        'viewRateSumStart': "",
                        }
                    r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                    # print(r.json())
                    total=r.json()['merchantTotal']
                    time.sleep(2)
                    if total%50==0:
                        page=int(total/50)+1
                    else:
                        page=int(total/50)+2
                    for i in range(1,page):
                        data['index']=i
                        r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                        self.get_data(r)
                        time.sleep(3*random.random())
                        print("已成功存入第{}页店铺数据！".format(i))
                        
                elif month==11 or month==10:

                    data={
                         'approvedDateStart': "{}-{}-01".format(year,month),
                         'approvedDateEnd': "{}-{}-01".format(year,month+1),
                         'hot60CountEnd': "",
                         'hot60CountStart': "",
                         'index': 1,
                         'intervalRatingSumEnd': "",
                         'intervalRatingSumStart': "",
                         'merchant': "",
                         'merchantOrMname': "",
                         'mname': "",
                         'numEnteredEnd': "",
                         'numEnteredStart': "",
                         'numRatingEnd': "",
                         'numRatingStart': "",
                         'orderColumn': "view_rate_sum",
                         'pageSize': 50,
                         'ratingEnd': "",
                         'ratingStart': "",
                         'sort': "DESC",
                         'token': "",
                         'viewRateSumEnd': "",
                         'viewRateSumStart': "",
                         }
                    r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                    total=r.json()['merchantTotal']
                    time.sleep(2)
                    if total%50==0:
                        page=int(total/50)+1
                    else:
                        page=int(total/50)+2
                    for i in range(1,page):
                        data['index']=i
                        r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                        self.get_data(r)
                        time.sleep(3*random.random())
                        print("已成功存入第{}页店铺数据！".format(i))                    
                else:
                    data={
                         'approvedDateStart': "{}-{}-01".format(year,month),
                         'approvedDateEnd': "{}-{}-01".format(year+1,1),
                         'hot60CountEnd': "",
                         'hot60CountStart': "",
                         'index': 1,
                         'intervalRatingSumEnd': "",
                         'intervalRatingSumStart': "",
                         'merchant': "",
                         'merchantOrMname': "",
                         'mname': "",
                         'numEnteredEnd': "",
                         'numEnteredStart': "",
                         'numRatingEnd': "",
                         'numRatingStart': "",
                         'orderColumn': "view_rate_sum",
                         'pageSize': 50,
                         'ratingEnd': "",
                         'ratingStart': "",
                         'sort': "DESC",
                         'token': "",
                         'viewRateSumEnd': "",
                         'viewRateSumStart': "",
                         }
        
                    r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                    total=r.json()['merchantTotal']
                    time.sleep(2)
                    if total%50==0:
                        page=int(total/50)+1
                    else:
                        page=int(total/50)+2
                    for i in range(1,page):
                        data['index']=i
                        r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
                        self.get_data(r)
                        time.sleep(3*random.random())
                        print("已成功存入第{}页店铺数据！".format(i))

                    
        
                    
    def get_data(self,r):

        shop_data=r.json()['data']
        for data in shop_data:
            productCount=data['productCount']      # 商品总数
            numBought=data['numBought']            # 总销售数              
            approvedDate=data['approvedDate']      # 店铺开张时间
            hot60Count=data['hot60Count']          # 前60天新上架商品数
            intervalRatingSum=data['intervalRatingSum']     # 前30天新增评论数
            merchant=data['merchant']              # 店铺名
            mid=data['mid']                        # 店铺ID
            numEntered=data['numEntered']          # 总收藏数
            numRating=data['numRating']            # 总评论数
            rating=data['rating']                  # 评分
            viewRateGrowth=data['viewRateGrowth']  # 前7天浏览增幅百分比
            viewRateSum=data['viewRateSum']        # 前7天浏览增幅平均值
            item={
                      'productCount':productCount,
                      'numBought':numBought,
                      'approvedDate':approvedDate,
                      'hot60Count':hot60Count,
                      'intervalRatingSum':intervalRatingSum,
                      'merchant':merchant,
                      'mid':mid,
                      'numEntered':numEntered,
                      'numRating':numRating,
                      'rating':rating,
                      'viewRateGrowth':viewRateGrowth,
                      'viewRateSum':viewRateSum,
                      
                        }
        
            self.db['shop1'].insert_one(item)

    
        
if __name__=='__main__':
    
    a=shop()
    a.get_list()