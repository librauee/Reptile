# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:59:59 2019

@author: Administrator

东方网 部分html:    
    <li><a target="_blank" href="http://quote.eastmoney.com/sh201000.html">R003(201000)</a></li>
百度 部分html：
<div class="stock-info" data-spm="2">
    <div class="stock-bets">
        <h1>
            <a class="bets-name" href="/stock/sh600172.html">
            黄河旋风 (<span>600172</span>)
            </a>
            <span class="state f-up">已收盘 2019-02-11 &nbsp;15:00:12
            </span>
                    </h1>
        <div class="price s-up ">
                        <strong  class="_close">3.42</strong>
            <span>+0.14</span>
            <span>+4.27%</span>
                    </div>
        <div class="bets-content">
            
                                            <div class="line1">
                    <dl><dt>今开</dt><dd class="s-up">3.29</dd></dl>
                    <dl><dt>成交量</dt><dd>17.00万手</dd></dl>
                    <dl><dt>最高</dt><dd class="s-up">3.47</dd></dl>
                    <dl><dt>涨停</dt><dd class="s-up">3.61</dd></dl>
                    <dl><dt>内盘</dt><dd>6.43万手</dd></dl>
                    <dl><dt>成交额</dt><dd>5775.12万</dd></dl>
                    <dl><dt>委比</dt><dd>9.47%</dd></dl>
                    <dl><dt>流通市值</dt><dd>39.14亿</dd></dl>
                    <dl><dt class="mt-1">市盈率<sup>MRQ</sup></dt><dd>36.66</dd></dl>
                    <dl><dt>每股收益</dt><dd>0.07</dd></dl>
                    <dl><dt>总股本</dt><dd>14.51亿</dd></dl>
                    <div class="clear"></div>
                </div>   
"""

import re
import requests
from bs4 import BeautifulSoup

def getHTMLText(url,code='utf8'):
    print('开始获取url信息')
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status # 如果是200，表示返回的内容正确；如果不是200，会产生HttpError异常
        #如果已知网页的编码格式，可以修改自动识别的方式
        #r.encoding=r.apparent_encoding
        r.encoding=code
        #print(r.text[:1000])
        return r.text
    except:
        print ("urlError")
    print('完成url信息获取')
        
def getStockList(lst,stockURL):
    print('开始获取东方网上的股票列表')
    html=getHTMLText(stockURL)
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find_all('a')
    for i in a:
        try:
            #个股的股票编号保存在lst中
            href=i.attrs['href']
            lst.append(re.findall(r'[s][hz]\d{6}',href)[0])
        except:
            continue
    print('获取股票列表完毕')

def getStockInfo(lst,stockURL,fpath):
    count=0;
    print('开始获取百度网上的股票信息')
    for stock in lst:
        url=stockURL+stock+".html"
        html=getHTMLText(url)
        try:
            if html=="":
                continue
            #可能东方网上有的股票，在百度网上没有，用东方网上的股票list匹配百度网时可能出现空页面
            infoDict={}
            soup=BeautifulSoup(html,'html.parser')
            stockInfo=soup.find('div',attrs={'class':'stock-bets'})
            name=stockInfo.find_all(attrs={'class':'bets-name'})[0]   
            #find_all返回列表，加上[0],表示返回sz519835,而不是[sz519835]
            infoDict.update({'股票名称':name.text.split()[0]})
            #找到股票信息的两个键、值标签
            keyList=stockInfo.find_all('dt')
            valueList=stockInfo.find_all('dd')            
            #将键值对还原成键值对，并存到字典中
            for i in range(len(keyList)):
                key=keyList[i].text
                value=valueList[i].text
                infoDict[key]=value
            with open(fpath,'a',encoding='utf8') as f:
                f.write(str(infoDict)+'\n')
                count+=1
                print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
        except:
            count+=1
            print('\rspeed:{:.2f}%'.format(count*100/len(lst)),end='')
            continue
    print('完成股票信息提取')


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'D://BaiduStockInfo.txt'
    slist=[]#股票信息
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)
    
if __name__=='__main__':
    main()

    
