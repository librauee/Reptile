# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 16:14:41 2019

@author: Lee
"""

import requests
import time
import json
from PIL import Image
import matplotlib.pyplot as plt



class Beauty(object):
    
    def __init__(self):
        """
        初始化，获取验证码链接
        """
        now=int(time.time())
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        self.origin_url='https://www.faceplusplus.com.cn/api/official/captcha/get?{}'.format(now)
        self.url='https://www.faceplusplus.com.cn/api/official/demo/facepp/v3/detect'

        
    def get_cookies(self):
        """
        验证码下载到本地，并且获取cookie信息
        """        
        session=requests.session()
        r=session.get(self.origin_url,headers=self.headers)
        with open ('a.jpg','wb') as f:
            f.write(r.content)
            
        return session
    
    def get_score(self):
        """
        输入图片url，获取颜值评分
        """
        
        session=self.get_cookies()
        flag=True
        image=Image.open('a.jpg')
        plt.imshow(image)
        plt.show()

        code=input("请输入验证码：")
        while flag:
            image_url=input("请输入照片链接(输入exit退出)：")
            if image_url=='exit':
                flag=False
                
            else:
                try:
                       
                    data={
                        'return_attributes': 'beauty,gender',
                        'beauty_score_min': '50',
                        'code': code,
                        'image_url': image_url
                         }
                    r=session.post(url=self.url,headers=self.headers,data=data)
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
                
                            print("您的颜值评分已经超过了地球上{}%的人！".format(score))                       
                except:
                    
                    print("您输入的图片链接格式有误，请重新输入！")

        
if __name__=='__main__':
    
    # image_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1575215938593&di=27e4c91f7c1584007cf5ab3939c0da31&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fq_mini%2Cc_zoom%2Cw_640%2Fimages%2F20170728%2F5843abd8cdb74745a2fe2349879cb055.jpeg'
    beauty=Beauty()
    beauty.get_score()

