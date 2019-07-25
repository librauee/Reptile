# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 08:23:11 2019

@author: Lee
"""


import re
import requests
import random
from fontTools.ttLib import TTFont
from lxml import etree
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import numpy as np


def mongo_configure():
    # Mongo配置
    conn=MongoClient('127.0.0.1', 27017)
    db=conn.job                    
    mongo_shixiseng=db.shixiseng
    return mongo_shixiseng

def parse_html(response,number):
    try:
        tree=etree.HTML(response)
        job=tree.xpath('//div[@class="f-l intern-detail__job"]/p/a/text()')
        salary=tree.xpath('//div[@class="f-l intern-detail__job"]/p/span[@class="day font"]/text()')
        city=tree.xpath('//div[@class="f-l intern-detail__job"]/p[@class="tip"]/span[@class="city ellipsis"]/text()')
        frequency=tree.xpath('//div[@class="f-l intern-detail__job"]/p[@class="tip"]/span[@class="font"]/text()')[::2]
        duration=tree.xpath('//div[@class="f-l intern-detail__job"]/p[@class="tip"]/span[@class="font"]/text()')[1::2]
        company_name=tree.xpath('//div[@class="f-r intern-detail__company"]/p/a/text()')
        # company_type=tree.xpath('//div[@class="f-r intern-detail__company"]/p/span[@class="ellipsis"]/text()')
        company_scale=tree.xpath('//div[@class="f-r intern-detail__company"]/p/span[@class="font"]/text()')
        # advantage=tree.xpath('//div[@class="clearfix advantage-wrap tip"]/div[@class="f-l"]/span//text()')
        advantage=[]   
        soup=BeautifulSoup(response,'html.parser')
        for i in soup.find_all('div',class_="clearfix advantage-wrap tip"):
            advantage.append(i.text)

        for i in range(len(job)):
            item={
              'job':job[i],
              'salary':salary[i],
              'city':city[i],
              'frequency':frequency[i],
              'duration':duration[i],
              'company_name':company_name[i],
              # 'company_type':company_type[i],
              'company_scale':company_scale[i],
              'advantage':advantage[i],
            }
            mongo_shixiseng.insert_one(item)
        print("已经成功抓取第{}页信息".format(number))
    except:
        print("抓取第{}页时出现问题，已经跳过此页！".format(number))
    
def get_dict():   
    '''
    输入：无
    输出：字体文件对应的字体字典（包含字体编码和对应字体）以及字体编码
    '''
    r=requests.get('https://www.shixiseng.com/interns/iconfonts/file')
    with open ('new_font.woff','wb') as f:
        f.write(r.content)

    # font1=TTFont('file2.woff')
    # font1.saveXML('font2.xml')
    font1=TTFont('new_font.woff')
    font1.saveXML('new_font.xml')
    # with open('font2.xml') as f:
    with open('new_font.xml') as f:
        xml=f.read()
    keys=re.findall('<map code="(0x.*?)" name="uni.*?"/>',xml)[:99]
    values=re.findall('<map code="0x.*?" name="uni(.*?)"/>',xml)[:99]
    for i in range(len(values)):
        if len(values[i])<4:
            values[i]=('\\u00'+values[i]).encode('utf-8').decode('unicode_escape')
        else:
            values[i]=('\\u'+values[i]).encode('utf-8').decode('unicode_escape')
    word_dict=dict(zip(keys, values))
    # print(word_dict)
    return word_dict,keys


def decrypt_font(response,keys):
    for key in keys:
        pattern='&#x'+key[2:]
        response=re.sub(pattern,word_dict[key],response)
    return response

    
if __name__=='__main__':    
    user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
     # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25", 
    ]
    url='https://www.shixiseng.com/interns/?keyword=%E7%AE%97%E6%B3%95&page={}&city=%E5%85%A8%E5%9B%BD'
    headers={"User-Agent": random.choice(user_agent),
             "Origin": "https://www.shixiseng.com",
            }
    word_dict,keys=get_dict()
    mongo_shixiseng=mongo_configure()
    for i in range(1,49):
        response=requests.get(url.format(i),headers=headers).text
        after_decrypt_response=decrypt_font(response,keys)
        parse_html(after_decrypt_response,i)
        time.sleep(10*np.random.rand())
    print("职位信息已全部入库！")

