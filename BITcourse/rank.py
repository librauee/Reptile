# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 10:04:18 2019

@author: Administrator
"""

import requests
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "爬取失败"
    
def fillUnivList(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
    #for tr in soup.find_all('tr',attr={'class':'alt'}):
        if isinstance(tr,bs4.element.Tag):
            tds=tr('td')
            ulist.append([tds[0].string,tds[1].string,tds[3].string])

def printUnivList(ulist,num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名","学校名称","总分",chr(12288))) 
    for i in range(num):       #做了优化，是输出的学校名称居中对齐，chr（12288）是汉字里面的空格
        u=ulist[i]
        print(tplt.format(u[0],u[1],u[2],chr(12288)))
    
def main():
    ulist=[]
    url='http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html'
    html=getHTMLText(url)
    fillUnivList(ulist,html)
    printUnivList(ulist,30)

#if __name__=='__main__':
main()   
    
            