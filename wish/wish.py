# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:23:08 2019

@author: Lee
"""

import requests
import json
from pymongo import MongoClient


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
        
        for i in range(1,101):
            data={
            'approvedDateEnd': "",
            'approvedDateStart': "",
            'hot60CountEnd': "",
            'hot60CountStart': "",
            'index': i,
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
            # print(r.status_code)
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
        
                self.db['shop'].insert_one(item)
            print("已成功存入第{}页店铺数据！".format(i))
    
        
if __name__=='__main__':
    
    a=shop()
    a.get_list()