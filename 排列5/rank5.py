# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 22:18:50 2019

@author: Administrator
"""

import requests
from lxml import etree

Submit='%BF%AA%CA%BC%B2%E9%BF%B4'

def decode(Submit):
    Submit=Submit.split('%')[1:]
    result=''
    for i in Submit:
        result+=str(int(i,base=16))
    return result

result=decode(Submit)
rank_1,rank_2,rank_3,rank_4,rank_5=[],[],[],[],[]


for i in range(2004,2019):
    url='https://www.cp121.com/pl5.asp'
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
         'accept-encoding': 'gzip, deflate, br',
         'cookie': 'ASPSESSIONIDQERDDRAQ=BGMEPKMCPIDEGLJHNHHDOOHD; __51cke__=; __tins__19199241=%7B%22sid%22%3A%201574345061249%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201574347769511%7D; __51laig__=2',}

    data={
      'Submitpl5':result,
      'cxqs':str(i)
      }
    r=requests.post(url,headers=headers,data=data)
    r.encoding=r.apparent_encoding
    tree=etree.HTML(r.text)
    number=tree.xpath('//tr[@align="center"]/td[@class="font3d1"]/text()|//tr[@align="center"]/td[@class="font3d2"]/text()')
    number="".join(number)
    rank_1.append(number[::5])
    rank_2.append(number[1::5])
    rank_3.append(number[2::5])
    rank_4.append(number[3::5])
    rank_5.append(number[4::5])
    print('number:')
    print(number)
print('rank1:')
print(rank_1)
print('rank2:')
print(rank_2)
print('rank3:')
print(rank_3)
print('rank4:')
print(rank_4)
print('rank5:')
print(rank_5)
    