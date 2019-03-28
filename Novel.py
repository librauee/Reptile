# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:02:49 2019

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
import sys

class download_txt(object):
    
    def __init__(self):
        self.url='http://www.biqukan.com'
        self.new_url = 'http://www.biqukan.com/3_3026/'
        self.names = []             #存放章节名
        self.urls = []              #存放每一个章节的链接
        self.nums = 0               #章节数目
    
    def get_url(self):
        
        try:
            r=requests.get(url=self.new_url,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            html=r.text
            #print(html)
            soup=BeautifulSoup(html,'html.parser')
            div=soup.find_all('div',class_='listmain')
            #print(div)
            a_bf=BeautifulSoup(str(div[0]),'html.parser')
            a=a_bf.find_all('a')
            self.nums=len(a[12:])
            for each in a[12:]:
                self.names.append(each.string)
                self.urls.append(self.url+each.get('href'))
            
        except:
            return "爬取链接失败"
        
    def get_contents(self,url):
        
        try:
            r=requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            html=r.text
            soup=BeautifulSoup(html,'html.parser')
            texts=soup.find_all('div',class_='showtxt')
            texts=texts[0].text.replace('\xa0'*8,'\n\n')
            return texts
        
        except:
            return "爬取文章内容失败"
        
    def save_txt(self,name,path,text):
        
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')
            
            
if __name__=='__main__':
    d=download_txt()
    d.get_url()
    print('开始下载小说《斗罗大陆》')

    for i in range(d.nums):
        
        d.save_txt(d.names[i],'斗罗大陆.txt',d.get_contents(d.urls[i]))
        sys.stdout.write("  已经下载：%.2f%%" % float(i/d.nums*100) + '\r')
        #sys.stdout.flush()
    print('《斗罗大陆》下载完成')
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

