# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:50:47 2019

@author: Lee
"""

import requests
import json
from pymongo import MongoClient


class G1(object):
    
    def __init__(self):
        
        self.url='http://www.haiyingshuju.com/wish_2.0/product/list'
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
             'Content-Length': '416'

             }
        self.db=MongoClient().wish
    
    def get_list(self):
        
        for i in range(1,5):
            data={
            'cids': "",                            # 商品所属类别 eg. ‘tag_53e9157121a8633c567eb0c1’
            'genTimeEnd': "",
            'genTimeStart': "",
            'hwc': "",
            'index': i,
            'intervalRatingEnd': "",
            'intervalRatingStart': "",
            'maxNumBoughtEnd': "",
            'maxNumBoughtStart': "",
            'merchant': "fengdiewangluo091",
            'merchantStatus': 1,
            'orderColumn': "max_num_bought",
            'pageSize': 50,
            'pb': "0",
            'pid': "",
            'pidStatus': 1,
            'pname': "",
            'pnameStatus': 1,
            'ratingEnd': "",
            'ratingStart': "",
            'sort': "DESC",
            'token': "",
            'totalpriceEnd': "",
            'totalpriceStart': "",
            'verified': "",
            'viewRateSumEnd': "",
            'viewRateSumStart': "",
            }
            r=requests.post(self.url,headers=self.headers,data=json.dumps(data))
            # print(r.status_code)
            shop_data=r.json()['data']
            for data in shop_data:
                
                if data['cidName']:
                    cidName=data['cidName']
                    cname=cidName[0]['cname']              # 最低级分类
                    pl1Name=cidName[0]['pl1Name']          # 第一级分类
                    pl2Name=cidName[0]['pl2Name']          # 第二级分类
                    pl3Name=cidName[0]['pl3Name']          # 第三级分类
                else:
                    cname=None
                    pl1Name=None
                    pl2Name=None
                    pl3Name=None
                hwc=data['hwc']                        # 是否是海外仓
                genTime=data['genTime']                # 上架时间
                rating=data['rating']                  # 评分              
                price=data['price']                    # 售价
                shipping=data['shipping']              # 运费
                pname=data['pname']                    # 产品名
                totalprice=data['totalprice']          # 总价
                verified=data['verified']              # 是否为wish认证，1为已认证
                pid=data['pid']                        # 商品ID
                numRating=data['numRating']            # 总评论数
                numEntered=data['numEntered']          # 总收藏数
                viewRateGrowth=data['viewRateGrowth']  # 前7天浏览增幅百分比
                viewRate1=data['viewRate1']        # 前7天浏览增幅平均值
                pb=data['pb']                          # 是否有PB
                feedTileText=data['feedTileText']      # 销售总数
                item={
                      'hwc':hwc,
                      'cname':cname,
                      'pl1Name':pl1Name,
                      'pl2Name':pl2Name,
                      'pl3Name':pl3Name,
                      'genTime':genTime,
                      'rating':rating,
                      'price':price,
                      'shipping':shipping,
                      'pname':pname,
                      'totalprice':totalprice,
                      'verified':verified,
                      'pid':pid,
                      'pb':pb,
                      'feedTileText':feedTileText,                      
                      'numEntered':numEntered,
                      'numRating':numRating,
                      'rating':rating,
                      'viewRateGrowth':viewRateGrowth,
                      'viewRate1':viewRate1,
                      
                        }
        
                self.db['fengdiewangluo091'].insert_one(item)
            print("已成功存入第{}页店铺数据！".format(i))
    
        
if __name__=='__main__':
    
    a=G1()
    a.get_list()