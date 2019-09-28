# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 20:40:31 2019

@author: Lee
"""

import requests
import re
import json
import time



url='https://wenku.baidu.com/view/925de78b9b89680202d82535.html'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
         'Cookie': 'Hm_lvt_59ce22710e353ee4d0f55960b28effd5=1561000430,1561000452; viewedPg=8b261078eef9aef8941ea76e58fafab069dc44c1%3D3%7C0%26552858ba1a37f111f1855b42%3D1%7C0%26d1a5ef8102d276a200292e93%3D1%7C0%2685208e06e2bd960590c677fd%3D1%7C0%268f7b1b73ba68a98271fe910ef12d2af90342a850%3D1%7C0%2634c2bee4227916888586d71c%3D1%7C0%26bee51c2eed630b1c59eeb514%3D6%7C0%26911653ae4b35eefdc9d33356%3D2%7C0%2678a0bc91aff8941ea76e58fafab069dc5122475f%3D1%7C0%26925de78b9b89680202d82535%3D1%7C0; wkview_gotodaily_tip=1; BAIDUID=A3D95C6AAE8BE8155A4E3BD5DF3F1081:FG=1; BIDUPSID=A3D95C6AAE8BE8155A4E3BD5DF3F1081; PSTM=1560647576; _click_param_pc_rec_doc_2017_testid=3; BDUSS=5qSFJoSEZhMnRveH5PYmQ1c1NkcllzR2tCZWZtMTloVVlYRkVxSG13RWQwcFZkRVFBQUFBJCQAAAAAAAAAAAEAAABQu9NKt8nM7LGssawAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB1Fbl0dRW5ddH; Hm_lvt_de54c5cc453c7904719695d12c1a5daa=1568120630,1568120734; delPer=0; PSINO=1; BDRCVFR[LyOqhVrki83]=mk3SLVN4HKm; ZD_ENTRY=baidu; session_name=www.baidu.com; isJiaoyuVip=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=5573342208; pgv_si=s507726848; Hm_lvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1569302730,1569570302,1569583675,1569583692; Hm_lpvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1569583692; session_id=1569583692654; H_PS_PSSID=1434_21092_18560_29523_29721_29567_29221_26350; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm',
         'Host': 'wenku.baidu.com',
         'Referer': 'https://www.baidu.com/link?url=EOcF9_rHtEsygCfLzjQRI7Tedh49ytjcp1v0KW0nx9voLXZECUPZUwixT6UPcTEWnuRD1GZ_TFRkDfmdfMHKvvJgqvLc45sN63dS70sZvkq&wd=&eqid=d1cd02a80001d308000000035d8dbd55'
}



r2=requests.get(url,headers=headers)
# print(r2.text)

#text=re.findall(r'FuZ2UiXX0(.*)\.1569636885',r2.text)[0]
token=re.findall('FuZ2UiXX0%3D\.(.*?)\%3D\.15696',r2.text)
bce_range=re.findall('&x-bce-range=(.*?)&token',r2.text)
timestamp=re.findall('15696(.*?)\\x22',r2.text)
timestamp='15696'+timestamp[0][:5]
host=re.findall('host%2F(.*?)&x-bce-range',r2.text)[0]
#print(bce_range)
#print(token)
#print(timestamp)
#print(host)
print(len(token))

 
def get_date() :

    time1=time.localtime(int(timestamp)-3600)
    time2=time.localtime(int(timestamp)-9*3600)
    dt1=time.strftime("%Y %H:%M:%S",time1)
    dt2=time.strftime("%Y-%m-%dT%H:%M:%S",time2)
    return dt1,dt2

dt1,dt2=get_date()

print(dt1)
print(dt2)



headers={
        'Referer': 'https://wenku.baidu.com/view/925de78b9b89680202d82535.html',
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
for i in range(10):

    idx=[]
    city=[]
    params={
        'responseContentType': 'application/javascript',
        'responseCacheControl': 'max-age=3888000',
        'responseExpires': 'Tue, 12 Nov {} +0800'.format(dt1),
        'authorization': 'bce-auth-v1/fa1126e91489401fa7cc85045ce7179e/{}Z/3600/host/{}'.format(dt2,host),
        'x-bce-range': bce_range[i],
        'token': 'eyJ0eXAiOiJKSVQiLCJ2ZXIiOiIxLjAiLCJhbGciOiJIUzI1NiIsImV4cCI6MTU2OTU5MTMyMiwidXJpIjp0cnVlLCJwYXJhbXMiOlsicmVzcG9uc2VDb250ZW50VHlwZSIsInJlc3BvbnNlQ2FjaGVDb250cm9sIiwicmVzcG9uc2VFeHBpcmVzIiwieC1iY2UtcmFuZ2UiXX0=.{}=.{}'.format(token[i],timestamp)      
        }
    url2='https://wkbjcloudbos.bdimg.com/v1/docconvert4933/wk/0b7a4e34545bdb3159178e1038607f80/0.json'
    r=requests.get(url2,headers=headers,params=params)
    # print(r.text)
    try:
        
        json1=r.text[8:-1]
        #json1=re.findall(r'wenku_1\((.*)\)',r.text)[0]
        data=json.loads(json1)
        print("___________________________________________________")
        # print(data['body'])
        body=data['body']
        lenth=len(body)

        for j in range(int(lenth/2)):
            idx.append(body[j]['c'])
            city.append(body[j+int(lenth/2)]['c'])
        
        dic=dict(zip(idx,city))

        print(dic)
        with open('file2.csv',"a") as f:
            [f.write('{0},{1}\n'.format(key, value)) for key, value in dic.items()]

    except:
       pass
     


#params={
#        'responseContentType': 'application/javascript',
#        'responseCacheControl': 'max-age=3888000',
#        'responseExpires': 'Tue, 12 Nov 2019 09:58:41 +0800',
#        'authorization': 'bce-auth-v1/fa1126e91489401fa7cc85045ce7179e/2019-09-28T01:58:41Z/3600/host/295711d4229a3250939d336d9617c7ee51e269d900fd1f2070ac73d127d78fd0',
#        'x-bce-range': '0-10019',
#        'token': 'eyJ0eXAiOiJKSVQiLCJ2ZXIiOiIxLjAiLCJhbGciOiJIUzI1NiIsImV4cCI6MTU2OTU5MTMyMiwidXJpIjp0cnVlLCJwYXJhbXMiOlsicmVzcG9uc2VDb250ZW50VHlwZSIsInJlc3BvbnNlQ2FjaGVDb250cm9sIiwicmVzcG9uc2VFeHBpcmVzIiwieC1iY2UtcmFuZ2UiXX0=.g6fzU2IkBdEQ6Z5+/5PGiwT5lMsrLgw8xv53kqpER/8=.1569639521'      
#        }
#url2='https://wkbjcloudbos.bdimg.com/v1/docconvert4933/wk/0b7a4e34545bdb3159178e1038607f80/0.json'
#r=requests.get(url2,headers=headers,params=params)
#print(r.text)
#json1=re.findall(r'wenku_1\((.*)\)',r.text)[0]
#data=json.loads(json1)
#print("___________________________________________________")
#print(data['body'])

