# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:37:21 2019

@author: Lee
"""

import requests
import time
import random
import numpy as np
from bs4 import BeautifulSoup


url='http://music.163.com/api/v1/resource/comments/R_SO_4_1374051000?&offset={}'
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
     # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25", 
]
    

headers = { 'User-Agent': random.choice(user_agent),  # 随机选取头部代理
            'Connection': "keep-alive",
            'Host': "music.163.com",
            'referer': 'https://music.163.com/download?type=sem&market=baidupz201901',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'cookie': '_ntes_nnid=933c525f8c0b999244d85429df9c54ed,1560650274521; _ntes_nuid=933c525f8c0b999244d85429df9c54ed; mail_psc_fingerprint=4c89f9e89b2b7fe2b11bf2c401bfd48d; _iuqxldmzr_=32; WM_TID=5QxWr%2Fu2t%2BBEAVBVQVYonyx1FwLGnWyT; P_INFO=lyc4481341234@163.com|1561010733|0|mail163|00&99|null&null&null#anh&340100#10#0#0|&0|urs&unireg|lyc4481341234@163.com; Province=0; City=0; hb_MA-891C-BF35BECB05C1_source=yuedu.163.com; hb_MA-BFF5-63705950A31C_source=www.baidu.com; JSESSIONID-WYYY=ddvhSSfrSNeDtI%2B7QSmNzjjGoZ3t1vkj0pBj5QPKQT%5Cv8PbPE0%2Fp9vWw%2F3Q3ytsN2goCOn1rWawKiTocORnsCGJOXfzNrF39ZJkBg3wXwc9m%5CGx%2FlrMyOMBmO7MiTz3tOgqV9HM%2F6cQmcv5hIdaarqlaW8k4KA3diwvca5Yq0jmxJiE%5C%3A1562570060948; WM_NI=UNoMQfJk5XZCy8J7MKJcLg2PwQ2pYg%2F%2FbUbgOIRXRtoI3YTpl9qcjH1zV4VSy21exMGdiapG%2FgZNSyOOPpXrIsAgcp95TvTyW%2Fm4WervQqqvffLXlTRf97Y0VgqwfSpfNG4%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebbd35b9aa7bc91cb74f4bc8ea7d55e878f8eaeb739b7879eaae63d869f86babc2af0fea7c3b92a9792a1aed46e8ab5fbb9d949bbe886d8d0418abd8488b15cb58ffe91dc6dedf1aeb6e16d8d979eb9d180ad97fdbad77cb0e7bf84e944f3a69ad5d559bbeeff86fb4785bca782f34dedb996afd2738d91a091db7a8bad8f88e27cfbeb9c97d77395f1a3d5d66fb2aa9f92f47ea6ba84b9ef6092baf7d8dc3c96b9bf98e559b4ba82a8b737e2a3'
          }


# 设置代理服务器
def get_ip_list(url, headers):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    ips = soup.find_all('tr')
    ip_list1 = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        #ip_list1.append('http://'+tds[1].text + ':' + tds[2].text)  #xici
        ip_list1.append('http://'+tds[0].text + ':' + tds[1].text)   #kuaidaili
    return ip_list1

# 判断代理服务器是否有效
def checkip(ip):

    url='http://www.baidu.com/'
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    try:
        r=requests.get(url,headers=headers,proxies={'http':ip},timeout=5)
        if r.status_code==200:   
            return True
        else:
            return False
    except:
        return False


    
def select_good_ip(ip_list,good_ip_list):
    for ip in ip_list:
        if checkip(ip):
            good_ip_list.append({'http': ip})





def getjson(url,proxy):
    try:
        #r=requests.get(url,headers=headers,timeout=30,proxies=random.choice(good_ip_list))
        r=requests.get(url,headers=headers,proxies={'https': 'https://{}:{}'.format(proxy['ip'], proxy['port'])})
        r.encoding='utf-8'
        return r.json()
    except:
        return None
    
    
def main():
    offset=0
    '''
    good_ip_list = []
    ip_list=[]
    #proxy_url='http://www.xicidaili.com/nn/{}'  
    proxy_url='https://www.kuaidaili.com/free/inha/{}'    
    for i in range(1,6):
        ip_list.extend(get_ip_list(proxy_url.format(i), headers=headers))
    select_good_ip(ip_list,good_ip_list)
    print(good_ip_list)
    '''
    # 请求r1，获取随机代理IP
    r1=requests.get('http://47.100.21.174:8899/api/v1/proxies?limit=60').json()
    with open('music_comments.csv', 'a', encoding='utf-8_sig') as f:
        for i in range(10000):
            real_url=url.format(offset)
            proxy=random.choice(r1['proxies'])
            json=getjson(real_url,proxy)
            if json:
                comments=json['comments']
                for comment in comments:
            # 用户名
                    user_name = comment['user']['nickname'].replace(',', '，')
            # 用户ID
                    user_id = str(comment['user']['userId'])
            # 评论内容
                    com = comment['content'].strip().replace('\n', '').replace(',', '，')
            # 评论ID
                    comment_id = str(comment['commentId'])
            # 评论点赞数
                    praise = str(comment['likedCount'])
            # 评论时间
                    date = time.localtime(int(str(comment['time'])[:10]))
                    structed_date = time.strftime("%Y-%m-%d %H:%M:%S", date)
                    print(user_name, user_id,  com, comment_id, praise, structed_date)
                    f.write(user_name + ',' + user_id + ','+ com + ',' + comment_id + ',' + praise + ',' + structed_date + '\n')
                offset+=20

            # 加上随机的时间延迟
                
                rdtime=20*np.random.rand()
                time.sleep(rdtime)
                
    
if __name__ == '__main__':
    main()