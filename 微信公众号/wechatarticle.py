# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 21:51:21 2019

@author: Administrator
"""

import requests
import json
import time
from pymongo import MongoClient

url='http://mp.weixin.qq.com/mp/profile_ext'  

# Mongo配置
conn=MongoClient('127.0.0.1', 27017)
db=conn.wx                    #连接wx数据库，没有则自动创建
mongo_wx=db.article           #使用article集合，没有则自动创建

def get_wx_article(biz,uin,key,pass_ticket,appmsg_token,count=10):
    offset=1+(index+1)*11
    params={
        '__biz':biz,
        'uin':uin,
        'key':key,
        'offset':offset,
        'count':count,
        'action':'getmsg',
        'f':'json',
        'pass_ticket':pass_ticket,
        'scene':124,
        'is_ok':1,
        'appmsg_token':appmsg_token,
        'x5':0,
    }

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

    r=requests.get(url=url, params=params, headers=headers)
    resp_json=r.json()
    #print(resp_json)
    if resp_json.get('errmsg') == 'ok':
        # 是否还有分页数据，若没有更多数据则返回
        can_msg_continue=resp_json['can_msg_continue']
        # 当前分页文章数
        msg_count=resp_json['msg_count']
        print("当前分页共有{}篇文章".format(msg_count))
        general_msg_list=json.loads(resp_json['general_msg_list'])
        infolist=general_msg_list.get('list')
        print(infolist, "\n**************")
        for info in infolist:
            app_msg_ext_info=info['app_msg_ext_info']
            # 标题
            title=app_msg_ext_info['title']
            # 文章链接
            content_url=app_msg_ext_info['content_url']
            # 封面图
            cover=app_msg_ext_info['cover']
            # 发布时间
            datetime=info['comm_msg_info']['datetime']
            datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))

            mongo_wx.insert({
                'title': title,
                'content_url': content_url,
                'cover': cover,
                'datetime': datetime
            })
        if can_msg_continue==1:
            return True
        return False
    else:
        print('获取文章异常...')
        return False


if __name__ == '__main__':
    # 参数通过抓包获得
    biz=''
    uin=''
    key=''
    pass_ticket=''
    appmsg_token=''
    index=-1
    while 1:
        print(f'开始抓取公众号第{index + 1} 页文章.')
        flag=get_wx_article(biz,uin,key,pass_ticket,appmsg_token,index=index)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index+=1
        if not flag:
            print('该公众号文章已全部抓取并且存入本地数据库')
            break

        print('..........准备抓取公众号第 {} 页文章.'.format(index+2))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        