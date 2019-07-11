# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:06:24 2019

@author: Lee
"""

import json

with open("top250.json",'r',encoding='utf-8') as load_f:
    load_dicts = json.load(load_f)
    newdic={}
    for load_dict in load_dicts:
        newdic[load_dict['rank']]=load_dict['title']
print(newdic)