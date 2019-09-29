# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 13:53:53 2019

@author: Lee
"""

import requests
import re
import json
import time
import random
from pymongo import MongoClient
from pandas.io.json import json_normalize
from retry import retry

class Baidu_Wenku(object):
    
    def __init__(self):
        
        self.url1='https://wenku.baidu.com/view/925de78b9b89680202d82535.html'
        self.url2='https://wkbjcloudbos.bdimg.com/v1/docconvert4933/wk/0b7a4e34545bdb3159178e1038607f80/0.json'
        self.headers1={
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
             'Cookie': 'Hm_lvt_59ce22710e353ee4d0f55960b28effd5=1561000430,1561000452; viewedPg=8b261078eef9aef8941ea76e58fafab069dc44c1%3D3%7C0%26552858ba1a37f111f1855b42%3D1%7C0%26d1a5ef8102d276a200292e93%3D1%7C0%2685208e06e2bd960590c677fd%3D1%7C0%268f7b1b73ba68a98271fe910ef12d2af90342a850%3D1%7C0%2634c2bee4227916888586d71c%3D1%7C0%26bee51c2eed630b1c59eeb514%3D6%7C0%26911653ae4b35eefdc9d33356%3D2%7C0%2678a0bc91aff8941ea76e58fafab069dc5122475f%3D1%7C0%26925de78b9b89680202d82535%3D1%7C0; wkview_gotodaily_tip=1; BAIDUID=A3D95C6AAE8BE8155A4E3BD5DF3F1081:FG=1; BIDUPSID=A3D95C6AAE8BE8155A4E3BD5DF3F1081; PSTM=1560647576; _click_param_pc_rec_doc_2017_testid=3; BDUSS=5qSFJoSEZhMnRveH5PYmQ1c1NkcllzR2tCZWZtMTloVVlYRkVxSG13RWQwcFZkRVFBQUFBJCQAAAAAAAAAAAEAAABQu9NKt8nM7LGssawAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB1Fbl0dRW5ddH; Hm_lvt_de54c5cc453c7904719695d12c1a5daa=1568120630,1568120734; delPer=0; PSINO=1; BDRCVFR[LyOqhVrki83]=mk3SLVN4HKm; ZD_ENTRY=baidu; session_name=www.baidu.com; isJiaoyuVip=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=5573342208; pgv_si=s507726848; Hm_lvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1569302730,1569570302,1569583675,1569583692; Hm_lpvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1569583692; session_id=1569583692654; H_PS_PSSID=1434_21092_18560_29523_29721_29567_29221_26350; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm',
             'Host': 'wenku.baidu.com',
             'Referer': 'https://www.baidu.com/link?url=EOcF9_rHtEsygCfLzjQRI7Tedh49ytjcp1v0KW0nx9voLXZECUPZUwixT6UPcTEWnuRD1GZ_TFRkDfmdfMHKvvJgqvLc45sN63dS70sZvkq&wd=&eqid=d1cd02a80001d308000000035d8dbd55'
             }
        self.headers2={
            'Referer': 'https://wenku.baidu.com/view/925de78b9b89680202d82535.html',
            'Sec-Fetch-Mode': 'no-cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
     
        
    def get_proxy(self):
        
        conn=MongoClient('127.0.0.1', 27017)      
        db=conn.proxy
        mongo_proxy=db.good_proxy
        proxy_data=mongo_proxy.find()
        proxies=json_normalize([ip for ip in proxy_data])
        proxy_list=list(proxies['ip'])
        return proxy_list



        
        
    def get_token(self):
        
        r2=requests.get(self.url1,headers=self.headers1)
        # text=re.findall(r'FuZ2UiXX0(.*)\.1569636885',r2.text)[0]
        
        self.bce_range=re.findall('&x-bce-range=(.*?)&token',r2.text)
        # self.timestamp=re.findall('15696(.*?)\\x22',r2.text)
        # self.timestamp='15696'+self.timestamp[0][:5]
        self.timestamp=int(time.time())+3600
        self.token=re.findall('FuZ2UiXX0%3D\.(.*?)\%3D\.{}'.format(self.timestamp),r2.text)
        self.host=re.findall('host%2F(.*?)&x-bce-range',r2.text)[0]
        
    def get_date(self):
        
        time1=time.localtime(int(self.timestamp)-3600)
        time2=time.localtime(int(self.timestamp)-9*3600)
        dt1=time.strftime("%Y %H:%M:%S",time1)
        dt2=time.strftime("%Y-%m-%dT%H:%M:%S",time2)
        return dt1,dt2
    
#    @retry(tries=10,delay=3)     
#    def get_json(self,params,proxy_list):
#        
#        try:
#            proxy=random.choice(proxy_list)
#            r=requests.get(self.url2,headers=self.headers2,params=params,proxies={'https': 'https://{}'.format(proxy),'http':'http://{}'.format(proxy)})
#            json1=r.text[8:-1]
#            #json1=re.findall(r'wenku_1\((.*)\)',r.text)[0]
#            data=json.loads(json1)
#            print("___________________________________________________")
#            body=data['body']
#            lenth=len(body)
#            time.sleep(random.random())
#            return body,lenth
#        except:
#            print("当前页访问异常，正在重试中……")
#            time.sleep(3*random.random())
#            self.get_json(params)
    
    @retry(tries=10,delay=3)
    def get_json(self,params,proxy_list):
        
        proxy=random.choice(proxy_list)
        r=requests.get(self.url2,headers=self.headers2,params=params,proxies={'https': 'https://{}'.format(proxy),'http':'http://{}'.format(proxy)})
        if len(r.text)>600:
            return r.text
        else:
            print("当前页访问异常，正在重试中……")
            time.sleep(5*random.random())
            self.get_json(params,proxy_list)


    
    def main(self):
        
        dt1,dt2=self.get_date()
        proxy_list=self.get_proxy()
        for i in range(75):
            idx=[]
            city=[]
            params={
               'responseContentType': 'application/javascript',
               'responseCacheControl': 'max-age=3888000',
               'responseExpires': 'Wed, 13 Nov {} +0800'.format(dt1),
               'authorization': 'bce-auth-v1/fa1126e91489401fa7cc85045ce7179e/{}Z/3600/host/{}'.format(dt2,self.host),
               'x-bce-range': self.bce_range[i],
               'token': 'eyJ0eXAiOiJKSVQiLCJ2ZXIiOiIxLjAiLCJhbGciOiJIUzI1NiIsImV4cCI6MTU2OTU5MTMyMiwidXJpIjp0cnVlLCJwYXJhbXMiOlsicmVzcG9uc2VDb250ZW50VHlwZSIsInJlc3BvbnNlQ2FjaGVDb250cm9sIiwicmVzcG9uc2VFeHBpcmVzIiwieC1iY2UtcmFuZ2UiXX0=.{}=.{}'.format(self.token[i],self.timestamp)      
        }

            text=self.get_json(params,proxy_list)
            
            data=json.loads(text[text.find('{'):-1])
            print("___________________________________________________")
            body=data['body']
            lenth=len(body)
            time.sleep(random.random())
            
            print("已经成功爬取第{}页信息".format(i+1))
            for j in range(int(lenth/2)):
                idx.append(body[j]['c'])
                city.append(body[j+int(lenth/2)]['c'])
        
            dic=dict(zip(idx,city))

            print(dic)
            with open('file.csv',"a") as f:
                [f.write('{0},{1}\n'.format(key, value)) for key, value in dic.items()]
                
                
                
if __name__=='__main__':
    
    crawler=Baidu_Wenku()
    crawler.get_token()
    crawler.main()
    