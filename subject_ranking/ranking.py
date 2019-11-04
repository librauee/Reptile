# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 11:15:30 2019

@author: Administrator
"""

import requests
from lxml import etree
from pymongo import MongoClient



class best(object):
    
    def __init__(self):
        self.link_url='http://www.zuihaodaxue.com/best_chinese_subjects_rankings.html'
        self.base_url='http://www.zuihaodaxue.com/'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.collect=MongoClient().ranking
        
    def get_links(self):
        r=requests.get(self.link_url,headers=self.headers)
        tree=etree.HTML(r.text)
        links=tree.xpath('//div[@class="subject-ranking-content"]/a/@href')
        # 2017-2019三年排名url
        links=[self.base_url+i[2:] for i in links]
        #links=[self.base_url+i[2:].replace('2019','2018') for i in links]
        #links=[self.base_url+i[2:].replace('2019','2017') for i in links]
        return links
        
    def get_rankings(self):
        links=self.get_links()

        for link in links:
            try:
                r=requests.get(link,headers=self.headers)
                r.encoding=r.apparent_encoding
                tree=etree.HTML(r.text)
                subject=tree.xpath('//span[@class="post-title"]/text()')[0][15:-1]
                ranking=tree.xpath('//tr[@class="bgfd"]/td[1]/text()')
                #ranking_last_year=tree.xpath('//tr[@class="bgfd"]/td[2]/text()')
                percent=tree.xpath('//tr[@class="bgfd"]/td[3]/text()')
                school=tree.xpath('//tr[@class="bgfd"]/td[4]/text()')
                score=tree.xpath('//tr[@class="bgfd"]/td[7]/text()')

                for i in range(len(ranking)):
                    item={
                        'subject':subject,
                        'ranking':ranking[i],
                        'percent':percent[i],
                        'school':school[i],
                        'score':score[i],
                        
                        }            
            
                    self.collect['subjects'].insert_one(item)
                print("已经把{}学科的排名数据存入！".format(subject))
            except:
                print(link)
        
        
if __name__=='__main__':
    rank=best()
    rank.get_rankings()