# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:31:53 2019

@author: Administrator
bz: "调剂特殊要求"
dwdm: "单位代码"
dwmc: "单位名称"
fbsjStr: "发布时间"
gxsj: "距离最后更新时间已过xx分钟"
hasit: "考生是否已经填报该志愿 true 或 false"
id: "余额信息ID"
qers: "余额人数"
sfmzyq: "是否满足要求，空为满足要求，非空其内容为不满足要求原因"
ssdm: "省市代码"
xxfs: "学习方式"
yjfxdm: "研究方向代码"
yjfxmc: "研究方向名称"
yxsdm: "院系所代码"
yxsmc: "院系所名称"
zt: "余额状态"
zydm: "专业代码"
zymc: "专业名称"
"""

import requests
import json
import os
from pymongo import MongoClient
import pandas as pd



count=0
count1=0
url='https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action'

headers={
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://yz.chsi.com.cn',
            'Referer': 'https://yz.chsi.com.cn/sytj/tj/qecx.html',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
            'Cookie':''
}   
type_dict = {}
type_dict['1'] = "全日制"
type_dict['2'] = "非全日制"


                  
def parse_one_page(content):

    for item in content:
        yield{
            'school': item['dwmc'],
            'academic': item['yxsmc'],
            'major': item['zymc'],
            'majorID': item['zydm'],
            'schoolID': item['dwdm'],
            'direction':item['yjfxmc'],
            'type':type_dict[str(item['xxfs'])],
            'remain':item['qers'],
            'publish':item['gxsj']
        }
       
with open('tjinfo.csv', 'a', encoding='utf-8') as csv:
    csv.write('学校编号'+','+'学校名称'+','+'所属学院'+','+'专业名称'+','
              +'专业代码'+','+'研究方向'+','+'培养类型'+','
              +'计划人数'+','+'距离最后更新时间已过分钟'+'\n')       
for i in range(60):
    if count==0:
        para={
         'pageSize': 20,
         'start': '',
         'orderBy':'' ,
         'mhcx': 1,
         'ssdm2': '',
         'xxfs2': '',
         'dwmc2': '计算机',
         'data_type': 'json',
         'agent_from':'wap',
         'pageid': ''
        }
    else:
        para={
         'pageSize': 20,
         'start': count*20,
         'orderBy':'' ,
         'mhcx': 1,
         'ssdm2': '',
         'xxfs2': '',
         'dwmc2': '计算机',
         'data_type': 'json',
         'agent_from':'wap',
         'pageid': 'tj_qe_list' 
            
            }
    try:
        r=requests.post(url,headers=headers,timeout=30,data=para)
        count+=1
        r.raise_for_status()
        r.encoding='utf-8'
        #print (r.text)      
        text=json.loads(r.text)
        content=text['data']['vo_list']['vos']
        #print(content)
    except:
        count+=1

    
    for item in parse_one_page(content): 
        with open('tjinfo.csv', 'a', encoding='utf-8') as csv:
            csv.write(item['schoolID'] + ',' + item['school'] +','+ 
                       item['academic'] + ',' + item['major'] + ','+ item['majorID']+',' +
                       item['direction']+ ',' + str(item['type'])+','+str(item['remain'])+','+str(item['publish'])+'\n')


for i in range(60):
    if count1==0:
        para={
         'pageSize': 20,
         'start': '',
         'orderBy':'' ,
         'mhcx': 1,
         'ssdm2': '',
         'xxfs2': '',
         'dwmc2': '软件',
         'data_type': 'json',
         'agent_from':'wap',
         'pageid': ''
        }
    else:
        para={
         'pageSize': 20,
         'start': count1*20,
         'orderBy':'' ,
         'mhcx': 1,
         'ssdm2': '',
         'xxfs2': '',
         'dwmc2': '软件',
         'data_type': 'json',
         'agent_from':'wap',
         'pageid': 'tj_qe_list' 
            
            }
    try:
        r=requests.post(url,headers=headers,timeout=30,data=para)
        count1+=1
        r.raise_for_status()
        r.encoding='utf-8'
        #print (r.text)      
        text=json.loads(r.text)
        content=text['data']['vo_list']['vos']
        #print(content)
    except:
        count1+=1

    
    for item in parse_one_page(content): 
        with open('tjinfo.csv', 'a', encoding='utf-8') as csv:
            csv.write(item['schoolID'] + ',' + item['school'] +','+ 
                       item['academic'] + ',' + item['major'] + ','+ item['majorID']+',' +
                       item['direction']+ ',' + str(item['type'])+','+str(item['remain'])+','+str(item['publish'])+'\n')                
    
print("存入csv文件完成")


             


'''
host = os.environ.get('MONGODB_HOST', '127.0.0.1')  # 本地数据库
port = os.environ.get('MONGODB_PORT', '27017')  # 数据库端口
mongo_url = 'mongodb://{}:{}'.format(host, port)
mongo_db = os.environ.get('MONGODB_DATABASE', 'yanzhaotj')
client = MongoClient(mongo_url)
db = client[mongo_db]
#db['yanzhaotj'].create_index('yjfxdm')

data={'school':content['dwmc'],'academic':content['yxsmc'],'major':content['zymc'],'direction':content['yjfxmc']
      }

db['yanzhaotjl].insert_one(data)
'''
