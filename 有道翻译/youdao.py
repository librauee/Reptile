# -*- coding: utf-8 -*-
"""
Created on Wed Jul 3 13:16:37 2019

@author: Lee
"""
import requests
import time
import hashlib
import random

class youdao_crawl():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=850665018@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=71221285.04687975; _ntes_nnid=6f09e5c54e440a52f10b177100aa9d1d,1561431366198; JSESSIONID=aaavC3vS98F0m-IjbuAVw; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abc32dNbypRD-5CwnJAVw; user-from=http://www.youdao.com/w/eng/%E8%8B%B9%E6%9E%9C/; from-page=http://www.youdao.com/w/eng/%E8%8B%B9%E6%9E%9C/; ___rl__test__cookies=1562740161910'
          }
        self.data = {
            'i': None,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': None,
            'sign': None,
            'ts': None,
            'bv': None,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
          }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        
    def translate(self, word):
        ts = str(int(time.time()*10000))
        salt = str(int(time.time()*10000) + random.random()*10 + 10)
        sign = 'fanyideskweb' + word + salt + '97_3(jkMYg@T[KZQmqjTK'
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['ts'] = ts
        self.data['bv'] = bv
        re = requests.post(self.url, headers=self.headers, data=self.data)
        return re.json()['translateResult'][0][0].get('tgt')
    
    
if __name__ == '__main__':
    youdao = youdao_crawl()
    while True:
        content = input("请输入您需要翻译的内容:")
        if content == "q":
            break
        trans = youdao.translate(content)
        print(trans)