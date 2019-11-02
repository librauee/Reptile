# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 11:15:30 2019

@author: Administrator
"""

import requests
from lxml import etree

class best(object):
    
    def __init__(self):
        self.link_url='http://www.zuihaodaxue.com/best_chinese_subjects_rankings.html'
        self.base_url='http://www.zuihaodaxue.com/'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
      
    def get_links(self):
        r=requests.get(self.link_url,headers=self.headers)
        tree=etree.HTML(r.text)
        links=tree.xpath('//div[@class="subject-ranking-content"]/a/@href')
        links=[self.base_url+i[2:] for i in links]
        return links
        
    def get_rankings(self):
        links=self.get_links()[:2]
        for link in links:
            r=requests.get(link,headers=self.headers)
            r.encoding=r.apparent_encoding
            tree=etree.HTML(r.text)
            subject=tree.xpath('//span[@class="post-title"]/text()')[0][15:]
            ranking=tree.xpath('//tr[@class="bgfd"]/td[1]')
            ranking_last_year=tree.xpath('//tr[@class="bgfd"]/td[2]')
            percent=tree.xpath('//tr[@class="bgfd"]/td[3]')
            school=tree.xpath('//tr[@class="bgfd"]/td[4]')
            score=tree.xpath('//tr[@class="bgfd"]/td[7]')
            print(subject)
        
        
if __name__=='__main__':
    rank=best()
    rank.get_rankings()