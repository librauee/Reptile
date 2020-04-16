# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:32:41 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

import requests
import base64
import tesserocr
from PIL import Image
from lxml import etree
import pandas as pd
from pymongo import MongoClient
import json
import threading

def ip_img(img_base64,i):
    
    img_data=base64.b64decode(img_base64)
    with open ('ip/{}.jpg'.format(i),'wb') as f:
        f.write(img_data)


def ocr_ip(img):
    image=Image.open(img)
    image=image.resize((450,60))
    image=image.convert('L')
    threshold=127
    table=[]
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
        
    image=image.point(table,'1')
    result=tesserocr.image_to_text(image).replace('§','5').replace('$','8').replace('L','1').replace('i','1').replace(',','')
    print(result)
    return result.replace('\n','')


def get_ip():
    
    ip=[]
    proxies=[]
    url='https://www.freeproxy.world/'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    for page in range(1,6):
        params={
            'type': '',
            'anonymity': '',
            'country': '',
            'speed': '',
            'port': '',
            'page': page
        }
        r=requests.get(url,headers=headers,params=params)
        tree=etree.HTML(r.text)
        img_base64=tree.xpath('//td[@class="show-ip-div"]/img/@src')
        print(img_base64[0])
        for i in range(len(img_base64)):
            ip_img(img_base64[i][22:],i)
            ip.append(ocr_ip('ip/{}.jpg'.format(i)))
        
        data=tree.xpath('//td/a/text()')
        Port=data[::6]
        Type=[i.strip() for i in data[4::6]]
        Anonymity=[i.strip() for i in data[5::6]]
    
        for i in range(len(Port)):
            if Anonymity[i]=='High':
                proxies.append('{}://{}:{}'.format(Type[i],ip[i],Port[i]))
            
    return proxies
            
# df=pd.DataFrame({'IP':ip,'Port':Port,'Type':Type,'Anonymity':Anonymity})
    # db=MongoClient().proxy
    # db['new'].insert(json.loads(df.T.to_json()).values())
    
    
def check_ip(proxy):
    
    try:
        url='http://ip.tool.chinaz.com/'
        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        r1=requests.get(url,headers=headers,proxies={'https':proxy,'http':proxy},timeout=30)
        tree=etree.HTML(r1.text)
        ipaddress=tree.xpath('//dd[@class="fz24"]/text()')  
        print(ipaddress)

        if ipaddress[0] in proxy:
            return True
        else:
            return False
    except Exception as e:
        print(e)       
        return False
    
    
def get_ip_pool(proxy):
    
    if check_ip(proxy):
        print('{}可用'.format(proxy))
        db['1'].insert_one({'proxy':proxy})

    
if __name__=='__main__':
    
    db=MongoClient().proxy
    proxies=get_ip()
    print(proxies)
    
    tasks=[]
    for proxy in proxies:

        task=threading.Thread(target=get_ip_pool, args=(proxy,))
        tasks.append(task)
        task.start()        
    for _ in tasks:
        _.join()         
    print("完成代理ip验证并存储到本地！")    
    
