# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:20:53 2019

@author: Administrator
"""

import requests
import re
import json
import execjs
from pymongo import MongoClient
import time

class CBG(object):
    
    def __init__(self):
        
        self.url='https://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_rank&rank_type=31&page={}'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self.conn=MongoClient('127.0.0.1', 27017)
        self.db=self.conn.MHXY
        
    def get_json(self,i):
        r=requests.get(self.url.format(i),headers=self.headers)
        js=re.findall(r"var data = (.*);",r.text)[0]
        js=json.loads(js)
        return js
    
    def decode(self,data):
        with open('test.js','r') as f:
            javascript=f.read()
        ctx=execjs.compile(javascript)
        real_content=ctx.call('get_g',data)
        return real_content
    
    def get_highlights(self,data):
        highlights=data.encode().decode("unicode_escape")
        return highlights
    
    def get_equip_info(self,i):
        js=self.get_json(i)
        equip_list=js["equip_list"]
        for equip in equip_list:
            gem_level=equip['gem_level']
            large_equip_desc=self.decode(equip['large_equip_desc'])
            sum_dex=equip['sum_dex']
            create_time=equip['create_time']
            collect_num=equip['collect_num']
            highlights=self.get_highlights(equip['highlights'])
            price=equip['price']
            rank=equip['rank']
            expire_time=equip['expire_time']
            server_name=equip['server_name']
            item={
            'gem_level':gem_level,
            'large_equip_desc':large_equip_desc,
            'sum_dex':sum_dex,
            'create_time':create_time,
            'collect_num':collect_num,
            'highlights':highlights,
            'price':price,
            'rank':rank,
            'expire_time':expire_time,
            'server_name':server_name
            }
            self.db['cbg'].insert_one(item)
            
            
            
            
if __name__=='__main__':
    
    mhxycbg=CBG()
    for i in range(1,11):
        mhxycbg.get_equip_info(i)
        time.sleep(1)
        print("第{}页装备信息已存入数据库！".format(i))