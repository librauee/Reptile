# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 10:02:37 2019

@author: Lee
"""

# 获取该分类下的所有书籍的名字和书籍的id清单
import requests
from bs4 import BeautifulSoup

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
url='http://yuedu.163.com/book/category/category/2100/2110/1_0_1/'
newbookid1=[]
newbookid2=[]
newbookid=[]
name=[]

for i in range(1,27):
    new_url=url+'p'+str(i)+'/s20'
    r=requests.get(new_url,headers=headers,timeout=30)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    soup=BeautifulSoup(r.text,'html.parser')   
    t=soup.find(attrs={'class':'g-bdw g-bdw-1'})
    for ti in t.findAll('h2')[:20]:
        name.append(ti.text)
    for j in soup.find_all(attrs={'class':'yd-book-item yd-book-item-pull-left'}):
        bookid=[]
        for k in j.find_all('a'):
            bookid.append(k.get('href'))
        for idx in bookid:
            a=idx[8:]
            newbookid1.append(a)
    for j in soup.find_all(attrs={'class':'yd-book-item yd-book-item-pull-left edge-right'}):
        bookid=[]
        for k in j.find_all('a'):
            bookid.append(k.get('href'))
        for idx in bookid:
            a=idx[8:]
            newbookid2.append(a)
for i in range(len(newbookid1)):
    newbookid.append(newbookid1[i])
    newbookid.append(newbookid2[i])
    
print(newbookid)
print(name)
