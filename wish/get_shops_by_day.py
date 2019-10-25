# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:32:13 2019

@author: Lee

利用小象代理，一次提取一个IP

按店铺开张时间为查询条件爬取wish全平台店铺数据
"""

import requests
import json
from pymongo import MongoClient
import time

class shop(object):
    
    def __init__(self):
        
        self.url='http://www.haiyingshuju.com/wish_2.0/merchant/list'
        self.headers={
             'Cookie': '',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',             
             'Host': 'www.haiyingshuju.com',
             'Origin': 'http://www.haiyingshuju.com',
             'token':'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjM3MDcyLCJzdWIiOiJsaWJyYXVlZSIsImNyZWF0ZWREYXRlIjoxNTcxNzkzODYyNzk1LCJpc3MiOiJoeXNqIiwiZXhwIjoxNTcxODAxMDYyLCJ1dWlkIjoiMGVkNDUyMTItNmRkYy00MDU0LWJhYzgtMTAzMmZjZGQzMTlkIiwiaWF0IjoxNTcxNzkzODYyfQ.4y8p1ZH2sNrUYTHosPz3q_5XxKkd-as_CedYbxEGgrSelDPMrBjaAKQaIEzaQTeum53AWSA7Ru3mE5xmg7xVDQ', 
             'Referer':'http://www.haiyingshuju.com/wish/index.html',
             'Content-Type': 'application/json;charset=UTF-8',
             'Accept': 'application/json, text/plain, */*',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
             'Connection': 'keep-alive',
             'Content-Length': '416'

             }
        self.db=MongoClient().wish
        self.date=[]
    
    def get_list(self):
        #self.proxy_list=['183.129.244.16:'+str(i) for i in [21862, 19452, 12062, 19314, 14852, 13340, 12098, 17351, 22259, 22317, 19992, 12305, 15977, 19585, 17130, 11393, 11262, 14726, 15886, 19109, 16789, 17878, 18396, 16930, 15610, 19664, 12957, 19722, 21594, 16090, 12336, 20459, 11702, 17108, 20732, 19039, 17649, 11267, 13042, 14979, 18215, 19804, 19403, 18406, 16537, 11726, 12911, 14663, 21142, 13825, 13354, 21179, 15027, 21453, 20569, 20665, 21912, 20825, 15731, 20161, 14393, 12558, 11143, 20382, 16492, 14470, 18821, 11039, 22640, 21092, 18562, 13462, 11819, 18172, 21926, 17827, 13965, 11707, 14789, 19635, 19144, 15887, 13651, 13516, 17240, 16066, 12125, 12287, 16454, 11916, 14580, 20621, 17153, 19270, 11294, 19840, 12999, 22643, 22061, 20497]]
        self.proxy_list=requests.get('').json()['data'][0]
        day_list=[ '2018-12-21', '2018-12-22', '2018-12-23', '2018-12-24', '2018-12-25', '2018-12-26', '2018-12-27', '2018-12-28', '2018-12-29', '2018-12-30', '2018-12-31', '2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-05', '2019-01-06', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10', '2019-01-11', '2019-01-12', '2019-01-13', '2019-01-14', '2019-01-15', '2019-01-16', '2019-01-17', '2019-01-18', '2019-01-19', '2019-01-20', '2019-01-21', '2019-01-22', '2019-01-23', '2019-01-24', '2019-01-25', '2019-01-26', '2019-01-27', '2019-01-28', '2019-01-29', '2019-01-30', '2019-01-31', '2019-02-01', '2019-02-02', '2019-02-03', '2019-02-04', '2019-02-05', '2019-02-06', '2019-02-07', '2019-02-08', '2019-02-09', '2019-02-10', '2019-02-11', '2019-02-12', '2019-02-13', '2019-02-14', '2019-02-15', '2019-02-16', '2019-02-17', '2019-02-18', '2019-02-19', '2019-02-20', '2019-02-21', '2019-02-22', '2019-02-23', '2019-02-24', '2019-02-25', '2019-02-26', '2019-02-27', '2019-02-28', '2019-03-01', '2019-03-02', '2019-03-03', '2019-03-04', '2019-03-05', '2019-03-06', '2019-03-07', '2019-03-08', '2019-03-09', '2019-03-10', '2019-03-11', '2019-03-12', '2019-03-13', '2019-03-14', '2019-03-15', '2019-03-16', '2019-03-17', '2019-03-18', '2019-03-19', '2019-03-20', '2019-03-21', '2019-03-22', '2019-03-23', '2019-03-24', '2019-03-25', '2019-03-26', '2019-03-27', '2019-03-28', '2019-03-29', '2019-03-30', '2019-03-31', '2019-04-01', '2019-04-02', '2019-04-03', '2019-04-04', '2019-04-05', '2019-04-06', '2019-04-07', '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11', '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16', '2019-04-17', '2019-04-18', '2019-04-19', '2019-04-20', '2019-04-21', '2019-04-22', '2019-04-23', '2019-04-24', '2019-04-25', '2019-04-26', '2019-04-27', '2019-04-28', '2019-04-29', '2019-04-30', '2019-05-01', '2019-05-02', '2019-05-03', '2019-05-04', '2019-05-05', '2019-05-06', '2019-05-07', '2019-05-08', '2019-05-09', '2019-05-10', '2019-05-11', '2019-05-12', '2019-05-13', '2019-05-14', '2019-05-15', '2019-05-16', '2019-05-17', '2019-05-18', '2019-05-19', '2019-05-20', '2019-05-21', '2019-05-22', '2019-05-23', '2019-05-24', '2019-05-25', '2019-05-26', '2019-05-27', '2019-05-28', '2019-05-29', '2019-05-30', '2019-05-31', '2019-06-01', '2019-06-02', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06', '2019-06-07', '2019-06-08', '2019-06-09', '2019-06-10', '2019-06-11', '2019-06-12', '2019-06-13', '2019-06-14', '2019-06-15', '2019-06-16', '2019-06-17', '2019-06-18', '2019-06-19', '2019-06-20', '2019-06-21', '2019-06-22', '2019-06-23', '2019-06-24', '2019-06-25', '2019-06-26', '2019-06-27', '2019-06-28', '2019-06-29', '2019-06-30', '2019-07-01', '2019-07-02', '2019-07-03', '2019-07-04', '2019-07-05', '2019-07-06', '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-10', '2019-07-11', '2019-07-12', '2019-07-13', '2019-07-14', '2019-07-15', '2019-07-16', '2019-07-17', '2019-07-18', '2019-07-19', '2019-07-20', '2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26', '2019-07-27', '2019-07-28', '2019-07-29', '2019-07-30', '2019-07-31', '2019-08-01', '2019-08-02', '2019-08-03', '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08', '2019-08-09', '2019-08-10', '2019-08-11', '2019-08-12', '2019-08-13', '2019-08-14', '2019-08-15', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19', '2019-08-20', '2019-08-21', '2019-08-22', '2019-08-23', '2019-08-24', '2019-08-25', '2019-08-26', '2019-08-27', '2019-08-28', '2019-08-29', '2019-08-30']
        data1={
                        'approvedDateStart': "",
                        'approvedDateEnd': "",
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
                        'token': "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1aWQiOjM3MDcyLCJzdWIiOiJsaWJyYXVlZSIsImNyZWF0ZWREYXRlIjoxNTcxNzkzODYyNzk1LCJpc3MiOiJoeXNqIiwiZXhwIjoxNTcxODAxMDYyLCJ1dWlkIjoiMGVkNDUyMTItNmRkYy00MDU0LWJhYzgtMTAzMmZjZGQzMTlkIiwiaWF0IjoxNTcxNzkzODYyfQ.4y8p1ZH2sNrUYTHosPz3q_5XxKkd-as_CedYbxEGgrSelDPMrBjaAKQaIEzaQTeum53AWSA7Ru3mE5xmg7xVDQ",
                        'viewRateSumEnd': "",
                        'viewRateSumStart': "",
                        }
        count=0
        for i in day_list:
            
            
            data1['approvedDateStart']=i
            data1['approvedDateEnd']=i
            self.get_total(data1)
            count+=1
            if count%10==0:
                try:
                    self.proxy_list=requests.get('').json()['data'][0]
                except:
                    time.sleep(5)
                    self.proxy_list=requests.get('').json()['data'][0]
            print(self.date)
        

    def get_total(self,data1):
        
        

        proxy='{}:{}'.format(self.proxy_list['ip'],self.proxy_list['port'])
        print(proxy)
        #proxy=random.choice(self.proxy_list)

        try:
           r=requests.post(self.url,headers=self.headers,data=json.dumps(data1),proxies={'https': 'https://{}'.format(proxy),'http': 'http://{}'.format(proxy)},timeout=10)
           total=r.json()['merchantTotal']
           print(total)

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
            
               self.db['shop5'].insert_one(item)
           if total>50:
               if total%50==0:
                   page=int(total/50)+1
               else:
                   page=int(total/50)+2
               for i in range(2,page):
                   data1['index']=i
                   self.get_data(data1)
                   # time.sleep(3*random.random())
                   print("已成功存入第{}页店铺数据！".format(i))
           print("已成功存入{}创办的全部店铺数据".format(data1['approvedDateStart']))                
        
            
        except Exception as e:
            print(e)
            print("爬取失败")
            self.date.append(data1['approvedDateStart'])
            
        
                    
    def get_data(self,data1):
        proxy='{}:{}'.format(self.proxy_list['ip'],self.proxy_list['port'])
        #proxy=random.choice(self.proxy_list)
        try:
            r=requests.post(self.url,headers=self.headers,data=json.dumps(data1),proxies={'https': 'https://{}'.format(proxy),'http': 'http://{}'.format(proxy)},timeout=10)
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
        
                self.db['shop5'].insert_one(item)
        except:
            print("该页爬取失败")


    
        
if __name__=='__main__':
    
    a=shop()
    a.get_list()