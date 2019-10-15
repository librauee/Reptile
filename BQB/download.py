# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:21:38 2019

@author: Lee
"""

import requests
from redis import Redis
import os
import threading

class Download(object):
    
    def __init__(self):
        
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.r=Redis.from_url(url='redis://localhost?db=0', decode_responses=True)
        self.count=1

        
    def download(self):
        
                 
        if "urls" in self.r.keys():
            while True:
                try:
                    url=self.r.spop("urls")
                    r=requests.get(url,headers=self.headers)
                    with open(img_path+os.path.sep+'{}{}'.format(self.count,url[-4:]),'wb') as f:
                        f.write(r.content)                    
                    print("已经成功下载{}张表情包！".format(self.count))
                    self.count+=1
                except:
                    if "urls" not in self.r.keys():
                        print("表情包已全部下载完成")
                        break
                    else:
                        print("{}请求发送失败！".format(url))
                        continue
        else:
            self.download(self)
            
    

if __name__=='__main__':

    img_path='../BQBCollection'
    download=Download()
    tasks=[] 
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    for i in range(8):
        task=threading.Thread(target=download.download, )
        tasks.append(task)
        task.start()

    for _ in tasks:
        _.join()         
    print("完成图片爬取并存储到本地！")
