# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:00:07 2019

@author: Administrator
"""

import requests
import re


def getHTMLText(url,headers):
    try:
        r=requests.get(url,headers=headers,timeout=30)
        r.raise_for_status # 如果是200，表示返回的内容正确；如果不是200，会产生HttpError异常
        r.encoding=r.apparent_encoding# 将对文本中分析的编码来替换整体的编码
        #print(r.text[:1000])
        return r.text
    except:
        print ("urlError")
        


def parserPage(ilt,html):
    try:
        plt=re.findall(r'"view_price":"[\d.]*"',html)# 匹配键值对——"view_price":"[\d.]*"
        tlt=re.findall(r'"raw_title":".*?"',html) # *?表示前一个字符0或无限次扩展，最小匹配（只取到最后一个”为止的内容，这样就约束了匹配的内容就是商品本身的名字）
        '''
        去掉view_price字段，只取价格部分
        eval函数用来执行字符串表达式，并返回表达式的值（相当于将外面的双引号去掉）
        这里string.split(pattern)不是正则表达式re.split(pattern, string)，是将字符串分割，[1]是获得键值对的后面部分
        '''
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            ilt.append([price,title])
        #print(ilt)
    except:
        print ("parserError")
    
def printGoodsList(ilt):
    tplt="{:4}\t{:8}\t{:16}"# 定义输出格式的模板
    print(tplt.format("num","price","name"))
    count=0
    for g in ilt:
        count=count+1
        print(tplt.format(count,g[0],g[1]))
      
def main():
    goods='爬虫书'
    depth=3 # 爬取的深度，即有多个网页时决定爬几个网页
    headers = {"User_Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Cookie" : "登陆淘宝后F12在控制台中输入document.cookie获取Cookie"
}               
    start_url="https://s.taobao.com/search?q=" + goods
    infoList=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getHTMLText(url,headers)
            parserPage(infoList,html)
        except:
            continue
    printGoodsList(infoList)


main()




