# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 10:45:32 2020

@author: Administrator
"""

import requests


'https://leetcode.com/api/problems/all/'
headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
         'origin': 'https://leetcode-cn.com'
         }
url='https://leetcode-cn.com/graphql/'

data={"query":'query{question(titleSlug:"two-sum") {content,,likes,difficulty}}'}
r=requests.post(url,headers=headers,data=data)
question_data=r.json()
print(question_data)