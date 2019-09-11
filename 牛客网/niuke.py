# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:35:56 2019

@author: Lee
"""

import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import random
import time
import os
import threading
from retry import retry



class niuke(object):
    
    def __init__(self):
        
        self.url='https://www.nowcoder.com/discuss/tag/{}?type=2&page={}'
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        self.prefix='https://www.nowcoder.com'
        self.origin_url='https://www.nowcoder.com/discuss/tags?type=2'
        
    def get_enterprise(self):
        
        r=requests.get(self.origin_url,headers=self.headers)
        tree=etree.HTML(r.text)
        enterprise=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li/a/@data-href')
        enterprise_name=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li/a/span[@class="discuss-tag-item"]/text()')
        num=tree.xpath('//div[@data-nav="企业"]/ul[@class="discuss-tags-mod"]/li/span[@class="discuss-tag-num"]/text()')
        enterprise=[i[13:-7] for i in enterprise]
        num=[int(i[:-1]) for i in num]
        
        return enterprise,enterprise_name,num
 
    
    def get_href(self,enterprise,page):
        
        titles_new=[]
        r=requests.get(self.url.format(enterprise,page),headers=self.headers)
        tree=etree.HTML(r.text)
        hrefs=tree.xpath('//div[@class="discuss-main clearfix"]/a[1]/@href')
        titles=tree.xpath('//div[@class="discuss-main clearfix"]/a[1]/text()')
        hrefs=[self.prefix+href for href in hrefs]
        for title in titles:
            if title!='\n':
                titles_new.append(title.replace("\n","").replace("[","").replace("]","").replace("/","").replace("|"," ").replace("*","").replace("?","").replace("\\",",").replace(":",",").replace("<","").replace(">",""))

#        print(hrefs)
#        print(titles_new)
        return hrefs,titles_new
        
    def get_article(self,enterprise_name,hrefs,titles):
        
        for i in range(len(hrefs)):
            if os.path.exists('{}/{}.txt'.format(enterprise_name,titles[i])):
                pass
            else:
                r=requests.get(hrefs[i],headers=self.headers)
#            soup=BeautifulSoup(r.text,'html.parser')
#            text=soup.find(attrs={"class":"post-topic-des nc-post-content"})
#            text=str(text).replace("</div>","\n").replace("<div>","").replace("<br/>","").replace("<span>","").replace("</span>","")[44:]
                tree=etree.HTML(r.text)
                text=tree.xpath('string(//div[@class="post-topic-des nc-post-content"])')
                with open ('{}/{}.txt'.format(enterprise_name,titles[i]),'w',encoding='utf-8') as f:
                    f.write(text.replace("   ","\n"))
    

    @retry(tries=5,delay=0.5)          
    def main(self,enterprise,page,enterprise_name):
        
        hrefs,titles=self.get_href(enterprise,page)
        self.get_article(enterprise_name,hrefs,titles)



if __name__=='__main__':
    
    crawl=niuke()
    enterprise,enterprise_name,num=crawl.get_enterprise()
    
#    for j in range(len(enterprise)):
    for j in range(100):
        
        pages=int(num[j]/30)+2 if int(num[j]/30)<45 else 46
        if os.path.exists(enterprise_name[j]):
            pass
        else:
            os.mkdir(enterprise_name[j])

#        for page in range(1,pages):
#            print("开始抓取{}第{}页面经...".format(enterprise_name[j],page))
#            hrefs,titles=crawl.get_href(enterprise[j],page)
#            crawl.get_article(enterprise_name[j],hrefs,titles)
#            print("已经完成{}第{}页面经的抓取".format(enterprise_name[j],page))
#            time.sleep(random.random())
#            print("---------------------------------------------")
            
        tasks=[]
        for page in range(1,pages):
            print("开始抓取{}第{}页面经...".format(enterprise_name[j],page))
            task=threading.Thread(target=crawl.main,args=(enterprise[j],page,enterprise_name[j],))
            tasks.append(task)
            task.start()

        for _ in tasks:
            _.join() 
        print("已经成功抓取{}所有面经...".format(enterprise_name[j]))
        print("---------------------------------------------")




#url='https://www.nowcoder.com/discuss/254363'
#headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
#
#r=requests.get(url,headers=headers)
##tree=etree.HTML(r.text)
##text=tree.xpath('string(//div[@class="post-topic-des nc-post-content"])')
##print(text.replace(" ","\n"))
#
#
#soup=BeautifulSoup(r.text,'html.parser')
#text=soup.find(attrs={"class":"post-topic-des nc-post-content"})
#
#text=str(text).replace("</div>","\n").replace("<div>","").replace("<br/>","").replace("<span>","").replace("</span>","")[44:]
#print(text)