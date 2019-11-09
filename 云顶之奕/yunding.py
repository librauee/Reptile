# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 10:13:56 2019

@author: Lee
"""

import requests
import re
import demjson
from pymongo import MongoClient

class crawl_hero(object):
    
    def __init__(self):
        self.url='http://lol.duowan.com/s/zzqdata.js'
        self.headers={
                'Host': 'lol.duowan.com',
                'Referer': 'http://lol.duowan.com/1906/m_425042631560.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                }
        self.db=MongoClient().lol
        
    def get_json(self):
        
        r=requests.get(self.url,headers=self.headers)
#        a=re.sub('(// .*?\n)','',r.text)
#        a=re.sub('//purple,white, gold, blue, green','',a)
        json1=demjson.decode(r.text[9:-1])

        sorts_data=json1['hero']['sorts']
        for sorts in sorts_data:
            self.db['sorts'].insert_one(sorts)
        jobs_data=json1['hero']['jobs']
        for jobs in jobs_data:
            self.db['jobs'].insert_one(jobs)
        hero_data=json1['hero']['data']
        for hero in hero_data:
            color=hero['color']
            job=hero['job']
            name=hero['name']
            skill=hero['skill']
            sort=hero['sort']
            hero_dict={
                    'color':color,
                    'job':job,
                    'name':name,
                    'skill':skill,
                    'sort':sort
                    }
            self.db['hero'].insert_one(hero_dict)
            
        
if __name__=='__main__':
    
    crawl=crawl_hero()
    crawl.get_json()