# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:06:10 2019

@author: Lee
"""

import requests
from pymongo import MongoClient
import json
import re
import time
import random

class Crawler(object):
    
    def __init__(self):
        """
        初始化函数
        """
        self.headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.'
                                    '38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                    }
        # 配置mongodb数据库
        self.conn=MongoClient('127.0.0.1', 27017)
        self.db=self.conn.TecentVedio  

        # 1-30集  
        self.url1='https://union.video.qq.com/fcgi-bin/data?otype=json&tid=682&appid=20001238&appkey=6c03bbe9658448a4&union_platform=1&idlist=t00313mumzy,a00317z0pn4,z0031vqgrh3,w00314swosc,x0031q0gkn0,o0031p8w9ut,x0031w4tmz3,w0031dqweu3,z00311fdd7v,z0031yvi6rw,m0031uqtg1z,i00315xulbo,d00310bga17,e0031r8s7u9,k0031ogaf1o,o00310elvsc,v0031gnzvh7,y0031l73zrw,w0031dg6yts,k0031w7twmi,v0031ty0670,y0031qc33e2,g003114by65,e00318plmuw,d0031yl055h,y0031ls4oxf,d0031v122n5,s0031deflzd,k003141k5tn,n0031zcnfar&callback=jQuery191012174801096723575_1565328398974&_=1565328398981'                
        # 30-41集
        self.url2='https://union.video.qq.com/fcgi-bin/data?otype=json&tid=682&appid=20001238&appkey=6c03bbe9658448a4&union_platform=1&idlist=n0031zcnfar,b0031x9yun6,y0031sxf84y,q0031cvniyp,v0031v7ybc8,c00315gyvxf,j0031102kef,h0031vuiv9h,o0031248liy,a003128kcpi,i0031lmqvhz,j0031uzstj1,c00317aiyw6,b0904yv7z9g,b0905uikvt9,c00315f36q4,a0899sqx5sw,a00317wa133,a0901cczg7e,a09046oapim,a0031e5ki85,a0031eztxy3,a0031kanzx2,a0031myef1m,a0031q651ns,a0031r9ntdo,a0031s4fuqd,a0031sb30ay,a0906gzp197,b00312nezdk&callback=jQuery191012174801096723575_1565328398994&_=1565328398995'
        # xhr regist
        self.url3='https://access.video.qq.com/danmu_manage/regist?vappid=97767206&vsecret=c0bdcbae120669fff425d0ef853674614aa659c605a613a4&raw=1'
        self.pattern=r'targetid=(.*)&vid'

    def get_vedio_info(self):
        """
        获取视频相关信息，包括vid，时长duration,播放次数view_count
        """
        
        vedio_info=[]
        r1=requests.get(url=self.url1,headers=self.headers)        
        json1=json.loads(r1.text[r1.text.find('{'):-1])        
        results1=json1['results']
        episodes=[]
        for result in results1:
            episode=int(result['fields']['episode'])
            if episode!=0 and episode not in episodes:
                episodes.append(episode)
                title=result['fields']['title']
                view_count=result['fields']['view_all_count']
                vid=result['id']
                duration=int(result['fields']['duration'])
                vedio_info.append([title,episode,vid,view_count,duration])
                
                
        r2=requests.get(url=self.url2,headers=self.headers)
        json2=json.loads(r2.text[r2.text.find('{'):-1]) 
        results2=json2['results']
        for result in results2:
            episode=int(result['fields']['episode'])
            if episode!=0 and episode not in episodes:
                episodes.append(episode)
                title=result['fields']['title']
                view_count=result['fields']['view_all_count']
                vid=result['id']
                duration=int(result['fields']['duration'])
                vedio_info.append([title,episode,vid,view_count,duration])
        # print(vedio_info)        
        return vedio_info

    
    def get_target_id(self):
        """
        根据vid得到相应的target_id
        """

        episode=[]
        duration=[]
        vid=[]
        vedio_info=self.get_vedio_info()  
        for i in range(len(vedio_info)):
            episode.append(vedio_info[i][1])
            duration.append(vedio_info[i][4])
            vid.append(vedio_info[i][2])
   
        target_id=[]
        for i in range(len(vid)):
            data={
            'bIsGetUserCfg': 1,
            'mapExtData': {vid[i]:{"strCid":"xbd1y6fvwl3maoz","strLid":""}},
            'vecIdList': [vid[i]],
            'wRegistType': 2,
            'wSpeSource': 0            
             }
            resp=requests.post(url=self.url3,headers=self.headers,data=json.dumps(data))
            # print(resp.json())
            strDanMuKey=resp.json()['data']['stMap'][vid[i]]['strDanMuKey']
            target_id.append(re.findall(self.pattern,strDanMuKey)[0])
            # print(target_id)
        return target_id,episode,duration
    
    
    def get_danmu(self):
        """
        爬取一集《亲爱的，热爱的》电视剧的弹幕
        """
    
        target_list,episode_list,duration_list=self.get_target_id()
        for i in range(len(target_list)):
            
            url='http://mfm.video.qq.com/danmu?timestamp={}&target_id='+target_list[i]
            page=int(duration_list[i]/30)    

            for j in range(1,page+1):
                req_url=url.format(30*j)
                r=requests.get(req_url, headers=self.headers)
                for danmu in r.json(strict=False)['comments']:
                    self.parse_comment(danmu=danmu)               
                print("已存入第{}集第{}页弹幕信息".format(episode_list[i],j))
                time.sleep(random.random())
            print("*******************************\n已将第{}集弹幕信息存入数据库\n*******************************".format(episode_list[i]))
            time.sleep(5*random.random())
            
    def parse_comment(self, danmu):
        """
        解析函数，用来解析爬回来的json评论数据，并把数据保存进mongodb数据库
        """
        dmdic={
               'content': danmu['content'], 'id': danmu['commentid'],
               'upcount': danmu['upcount'],'timepoint': danmu['timepoint'],
               'username': danmu['opername'],'uservip_degree': danmu['uservip_degree'],
               'bbid': danmu['bb_id']              
               }  # 构造弹幕字典
        self.db['Danmu'].insert_one(dmdic)
        
        
    
    
if __name__=='__main__':
    
    dmcrawl=Crawler()
    dmcrawl.get_danmu()



    