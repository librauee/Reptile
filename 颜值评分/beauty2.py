# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:45:50 2019

@author: Administrator
"""

import requests
import time
import json
from PIL import Image
import matplotlib.pyplot as plt
from redis import Redis
from pymongo import MongoClient


class Beauty(object):
    
    def __init__(self):

        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        self.url='https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.r=Redis.from_url(url='redis://localhost?db=2', decode_responses=True)
        self.db=MongoClient().beauty

    def get_url(self):
        
                 
        if "urls" in self.r.keys():
            url=self.r.spop("urls")
            return url
        else:
            return 'exit'
    
    def get_score(self):
        """
        输入图片url，获取颜值评分
        """
        flag=True
        while flag:
            image_url=self.get_url()
            #image_url='https://pic3.zhimg.com/50/v2-44689b8b93ef7ba0730935e5884ac54f_hd.jpg'
            if image_url=='exit':
                flag=False
                
            else:

                try:
                       
                    data={
                        'api_key':'',
                        'api_secret':'',
                            
                        'return_attributes': 'beauty,gender',
                        'image_url': image_url
                         }
                    r=requests.post(url=self.url,headers=self.headers,data=data)
                    score_data=json.loads(r.text)
                    if len(score_data['faces'])==0:
                        print("未从该图片中找到人像！")
                    else:
                        face_num=score_data['face_num']
                        for i in range(face_num):
                            face=score_data['faces'][i]
                            beauty=face['attributes']['beauty']
                            gender=face['attributes']['gender']
                            if gender['value']=='Female':
                                score=beauty['female_score']
                            else:
                                score=beauty['male_score']
                            item={'image_url':image_url,
                                  'score':score
                                 }
                            self.db['score2'].insert_one(item)

                            print("您的颜值评分已经超过了地球上{}%的人！".format(score))   

                except Exception as e:
                    print(e)
                    print("您输入的图片链接格式有误，请重新输入！")


        
if __name__=='__main__':
    
    # image_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1575215938593&di=27e4c91f7c1584007cf5ab3939c0da31&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fq_mini%2Cc_zoom%2Cw_640%2Fimages%2F20170728%2F5843abd8cdb74745a2fe2349879cb055.jpeg'
    beauty=Beauty()
    beauty.get_score()
    