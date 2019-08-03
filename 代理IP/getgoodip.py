# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:27:42 2019

@author: Lee
"""

import requests
from bs4 import BeautifulSoup
import threading
from pymongo import MongoClient
from lxml import etree


def checkip(proxy):
    try:
        url='http://ip.tool.chinaz.com/'
        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        r1=requests.get(url,headers=headers,proxies={'https': 'https://{}'.format(proxy),'http': 'http://{}'.format(proxy)},timeout=30)
        tree=etree.HTML(r1.text)
        ipaddress=tree.xpath('//dd[@class="fz24"]/text()')  
        # print(ipaddress)

        if ipaddress[0]==proxy[:-5]:
            return True
        elif ipaddress[0]==proxy[:-6]:
            return True
        else:
            return False
    except:
        return False
    
    


def getgoodproxy(ip,ip_type):

    if checkip(ip):
        print('{}可用，类型为{}'.format(ip,ip_type))
        goodip.append(ip)
        handler.insert_one({'ip':ip})
        

if __name__ == '__main__':
    
    url='https://github.com/dxxzst/free-proxy-list'
    headers={ 'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")
    table=soup.find_all('table')[1]
    ulist1=[]
    ulist2=[]
    for tr in table.find_all('tr')[1:]:
        a=tr.text.split("\n")
        if a[4]=='high':
        # 'https': 'https://{}'.format(proxy)
            if a[3]=='http':
                ulist1.append("{}:{}".format(a[1],a[2]))
            else:
                ulist2.append("{}:{}".format(a[1],a[2]))

    goodip=[]
    client=MongoClient()
    db=client.proxy
    handler=db.good_proxy
    handler.delete_many({})  
    tasks=[]           # 线程池
    
    for ip1 in ulist1:
        task=threading.Thread(target=getgoodproxy, args=(ip1,'http',))
        tasks.append(task)
        task.start()
    
    for ip2 in ulist2:
        task=threading.Thread(target=getgoodproxy, args=(ip2,'https',))
        tasks.append(task)
        task.start()
        
        
    # 等待所有线程完成
    for _ in tasks:
        _.join()         
    print("完成代理ip验证并存储到本地！")
