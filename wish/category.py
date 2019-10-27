# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:53:13 2019

@author: Lee
"""

import requests
import json
from pymongo import MongoClient


class G1(object):
    
    def __init__(self):
        
        self.url='http://www.haiyingshuju.com/wish_2.0/category/list'
        self.headers={
             'Cookie': 'Hm_lvt_03a80b70183e649c063d5ee13290d51b=1570535053,1571050609,1571135610; JSESSIONID=2DFC98B05655485920D0DF2ED85B6566; Hm_lpvt_03a80b70183e649c063d5ee13290d51b=1571135709',
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
             'Content-Length': '634'

             }
        self.db=MongoClient().wish
    
    def get_list(self):
        
        for i in range(1,21):
            data={
            'cid': "",                            # 商品所属类别 eg. ‘tag_53e9157121a8633c567eb0c1’
            'fCid': "",
            'index': i,
            'intervalRatingSumEnd': "",
            'intervalRatingSumStart': "",
            'numEnteredEnd': "",
            'numEnteredStart': "",
            'numRatingEnd': "",
            'numRatingStart': "",
            'orderColumn': "view_rate_sum",
            'pageSize': 50,
            'product60numEnd': "",
            'product60numStart': "",   
            'sort': "DESC",
            'token': "",
            'viewRateSumEnd': "",
            'viewRateSumStart': "",
            }
            r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
            category_data=r.json()['data']
            for data in category_data:

                avgPrice=data['avgPrice']/100                    # 平均总价
                cid=data['cid']                                  # 类目ID
                cname=data['cname']                              # 类目名              
                fcid=data['fcid']                                # 一级类目ID
                fcname=data['fcname']                            # 一级类目名
                intervalRatingSum=data['intervalRatingSum']      # 前30天新增评论数
                merchantNum=data['merchantNum']                  # 商家总数
                numBought=data['numBought']                      # 总销售数
                product60num=data['product60num']                # 前60天新上架商品
                numRating=data['numRating']/1000000              # 总评论数
                numEntered=data['numEntered']                    # 总收藏数
                viewRateGrowth=data['viewRateGrowth']            # 前7天浏览增幅百分比
                viewRateSum=data['viewRateSum']                  # 前7天浏览平均值
                productNum=data['productNum']                    # 商品总数

                item={
                      'avgPrice':avgPrice,
                      'cname':cname,
                      'cid':cid,
                      'fcid':fcid,
                      'fcname':fcname,
                      'intervalRatingSum':intervalRatingSum,
                      'merchantNum':merchantNum,
                      'numBought':numBought,
                      'product60num':product60num,
                      'productNum':productNum,                    
                      'numEntered':numEntered,
                      'numRating':numRating,
                      'viewRateGrowth':viewRateGrowth,
                      'viewRateSum':viewRateSum,
                      
                        }
        
                self.db['category'].insert_one(item)
            print("已成功存入第{}页类目数据！".format(i))
    
        
if __name__=='__main__':
    
    a=G1()
    a.get_list()