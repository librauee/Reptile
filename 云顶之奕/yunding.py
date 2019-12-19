# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 10:13:56 2019

@author: Lee
"""

import requests
import re
import demjson
from pymongo import MongoClient
import pandas as pd

class crawl_hero(object):
    
    def __init__(self):
        self.url='http://lol.duowan.com/s/zzqdata.js'
        self.headers={
                'Host': 'lol.duowan.com',
                'Referer': 'http://lol.duowan.com/1906/m_425042631560.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                }
        self.db=MongoClient().lol1
        self.color_gold={ 
                'white':1,
                'green':2,
                'blue':3,
                'purple':4,
                'gold':5,
                'colorful':7
                }
        self.sort_info={
            'heroSort0':'剧毒',
            'heroSort2':'云霄',
            'heroSort3':'光',
            'heroSort4':'影',
            'heroSort5':'地狱火',
            'heroSort6':'森林',
            'heroSort7':'海洋',
            'heroSort8':'沙漠',
            'heroSort9':'钢铁',
            'heroSort10':'雷霆',
            'heroSort11':'山脉',
            'heroSort12':'水晶',
            'heroSort13':'极地',
            'heroJob0':'刺客',
            'heroJob2':'剑士',
            'heroJob3':'游侠',
            'heroJob4':'秘术',
            'heroJob5':'法师',
            'heroJob6':'大元素使',
            'heroJob7':'狂战士',
            'heroJob8':'守护神',
            'heroJob9':'掠食者',
            'heroJob10':'召唤使',
            'heroJob11':'德鲁伊',
            'heroJob12':'炼金师',
            
            }
        
    def get_json(self):
        
        r=requests.get(self.url,headers=self.headers)
        json1=demjson.decode(r.text[9:-1])
        hero_data=json1['hero']['data']
        count=0
        for hero in hero_data:
            info=[]
            hero_id=hero['id']
            color=hero['color']
            gold=self.color_gold[color]
            job=hero['job']
            job=job.split(',')
            name=hero['name']   
            name=name.replace(","," ")
            name=name.split()[-1]            
            names=name.split()
            sort=hero['sort']
            sort=sort.split(',')
            for i in sort:
                info.append(self.sort_info[i])
            for i in job:
                info.append(self.sort_info[i])
                
            
            hero_dict={
                    'hero_id':count,
                    'gold':gold,
                    'name':name,
                    'info':info
                    }
            self.db['hero'].insert_one(hero_dict)
            for i in range(len(names)):
                hero_short_dict={
                    'hero_id':count,
                    'name':names[i],
                    
                    }
            self.db['hero_short'].insert_one(hero_short_dict)
            count+=1
            
    def save(self):    
        
        data=list(self.db['hero'].find())
        df=pd.DataFrame(data)
        df=df.drop('_id',axis=1)
        df.to_csv('heros_info.csv', index=None, encoding='utf_8_sig')
        df=pd.DataFrame(list(self.db['hero_short'].find()))
        df=df.drop('_id',axis=1)
        df.to_csv('heros_info_short.csv', index=None, encoding='utf_8_sig')

            
        
if __name__=='__main__':
    
    crawl=crawl_hero()
    crawl.get_json()
    crawl.save()