# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 21:57:49 2019

@author: Administrator
"""

from bs4 import BeautifulSoup
import requests
import json
import time
from pymongo import MongoClient as Client


def dict2proxy(dic):
    s=dic['类型']+'://'+dic['ip']+':'+str(dic['端口'])
    print(s)
    return {'http':s,'https':s}


def getHTMLText(url,headers,code='utf-8'):
    try:
        r=requests.get(url,headers=headers,timeout=30)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return "url异常"
    
def getIP(html,ulist):
    
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('tr')[1:]
    #第一个不是ip
    
    for item in items:
        tds=item.find_all('td')
        ulist.append({'ip':tds[0].text,'端口':tds[1].text,'类型':tds[3].text,'位置':tds[4].text,'响应速度':tds[5].text,'最后验证时间':tds[6].text})
    #print(ulist)
    return ulist
            
            
                        
def saveAsJson(ulist):
    with open('proxy.json','w',encoding='utf-8') as f:
                json.dump(ulist,f,indent=7,ensure_ascii=False)#ensure_ascii参数使显示为中文
                
def saveAsJson1(ulist):
    with open('goodproxy.json','w',encoding='utf-8') as f:
                json.dump(ulist,f,indent=7,ensure_ascii=False) 
                
                
'''
def write_to_mongo(ip):
    client=Client(host='localhost',port=27017)
    db=client['proxies_db']
    coll=db['proxies']
    for i in ip:
        if coll.find({'ip':i['ip']}).count==0:
            coll.insert_one(i)
    client.close()
'''               
                
def checkip(ip):
    try:
        proxies=dict2proxy(ip)
        url='http://www.ipip.net/'
        headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        r=requests.get(url,headers=headers,proxies=proxies,timeout=5)
        r.raise_for_status()
    except:
        return False
    else:
        return True

def getgoodip(ip):
    goodip=[]
    for i in ip:
        if checkip(i):
            goodip.append(i)
    return goodip

                
def main():
    ulist=[]
    headers={'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
             'Accept-encoding':'gzip, deflate, br',
             'Accept-language':'zh-CN,zh;q=0.9',
             'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
    for num in range(1,11):
        url='https://www.kuaidaili.com/free/inha/%s' % num
        print("正在爬取第{}页".format(num))
        html=getHTMLText(url,headers)
        # time.sleep(5)  #增加间隔
        #print(html)
        iplist=getIP(html,ulist)
        saveAsJson(iplist)
    print("爬取完成！")
    print("开始检验ip")
    goodip=getgoodip(ulist)
    print("打印可以使用的ip:{}".format(goodip))
    print("开始存储可以使用的ip")
    saveAsJson1(goodip)
    print("完成存储")

  
    
if __name__ == '__main__':
    main()