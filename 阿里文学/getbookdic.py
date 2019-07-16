# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 07:09:41 2019

@author: Administrator
"""
import requests
import re
from bs4 import BeautifulSoup

url='https://www.aliwx.com.cn/store?page={}'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
         'referer': 'https://www.aliwx.com.cn/store'}
items=[]
for page in range(1,33):
    r=requests.get(url.format(page),headers=headers)
    soup=BeautifulSoup(r.text,'html.parser')
    for a in soup.find_all('a',{'class':'clear'}):
        bookname=a.attrs['title']
        bookid=a.attrs['href'][11:]
        item={
            #'bookname':bookname,
            #'bookid':bookid
            bookname:bookid
          }
        items.append(item)
print(items)
with open('booklist1.txt','w') as f:
    f.write(str(items))

