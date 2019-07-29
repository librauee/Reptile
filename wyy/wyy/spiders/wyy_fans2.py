# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:31:18 2019

@author: Lee
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:32:53 2019

@author: Administrator
"""

import scrapy
import random
import math
from Crypto.Cipher import AES
import codecs
import base64
import requests
from lxml import etree
from wyy.items import WyyItem
import json

class WyyFansSpider(scrapy.Spider):
    name = 'wyy_fans2'
    allowed_domains = ['163.com']
    # start_urls = ['http://163.com/']
    
    def __init__(self):
        self.key = '0CoJUm6Qyw8W8jud'
        self.f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.e = '010001'
        self.singer_id = '29879272'
        self.post_url1 = 'https://music.163.com/weapi/user/getfolloweds?csrf_token='
        self.post_url2 = 'https://music.163.com/weapi/v1/play/record?csrf_token='
    
    # 生成16个随机字符
    def _generate_random_strs(self,length):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        # 控制次数参数i
        i = 0
        # 初始化随机字符串
        random_strs  = ""
        while i < length:
            e = random.random() * len(string)
            # 向下取整
            e = math.floor(e)
            random_strs = random_strs + list(string)[e]
            i = i + 1
        return random_strs


    # AES加密
    def _AESencrypt(self,msg, key):
        # 如果不是16的倍数则进行填充(paddiing)
        padding = 16 - len(msg) % 16
        msg = msg + padding * chr(padding)
        # 用来加密或者解密的初始向量(必须是16位)
        iv = '0102030405060708'

        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 加密后得到的是bytes类型的数据
        encryptedbytes = cipher.encrypt(msg)
        # 使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)
        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf-8')

        return enctext


    # RSA加密
    def _RSAencrypt(self,randomstrs, key, f):
        # 随机字符串逆序排列
        string = randomstrs[::-1]
        # 将随机字符串转换成byte类型数据
        text = bytes(string, 'utf-8')
        seckey = int(codecs.encode(text, encoding='hex'), 16)**int(key, 16) % int(f, 16)
        return format(seckey, 'x').zfill(256)
    
    def _fans_total(self):
        url = 'https://music.163.com/user/fans?id={}'.format(self.singer_id)
        r = requests.get(url)
        tree = etree.HTML(r.text)
        total = tree.xpath('//strong[@id="fan_count"]/text()')
        return total[0]

    # 获取参数
    def _get_params1(self,page):
        offset = (page-1) * 20
        msg = '{"userId": "29879272", "offset":' + str(offset) + ', "total": "true", "limit": "20", "csrf_token": ""}'
        enctext = self._AESencrypt(msg, self.key)
        # 生成长度为16的随机字符串
        i = self._generate_random_strs(16)

        # 两次AES加密之后得到params的值
        encText = self._AESencrypt(enctext, i)
        # RSA加密之后得到encSecKey的值
        encSecKey = self._RSAencrypt(i, self.e, self.f)
        return encText, encSecKey
    
    
    def _get_params2(self,uid):
    
        msg = '{uid: ' + str(uid) + ', type: "-1", limit: "1000", offset: "0", total: "true", "csrf_token": ""}'
        enctext = self._AESencrypt(msg, self.key)
        # 生成长度为16的随机字符串
        i = self._generate_random_strs(16)

        # 两次AES加密之后得到params的值
        encText = self._AESencrypt(enctext, i)
        # RSA加密之后得到encSecKey的值
        encSecKey = self._RSAencrypt(i, self.e, self.f)
        return encText, encSecKey
    
    
    def start_requests(self):
        
        total_fans = self._fans_total()
        for i in range(1, int(int(total_fans) / 20) + 1):
            params, encSecKey = self._get_params1(i)
            formdata = {
                       'params': params, 'encSecKey': encSecKey
                       }
            yield scrapy.FormRequest(url = self.post_url1, formdata = formdata, callback = self.parse)

    def parse(self, response):
        response = json.loads(response.body)
        followeds = response['followeds']
        for followed in followeds:

            avatar = followed['avatarUrl']
            userId = followed['userId']
            vipType = followed['vipType']
            gender = followed['gender']
            eventCount = followed['eventCount']
            fan_followeds = followed['followeds']
            fan_follows = followed['follows']
            signature = followed['signature']
            time1 = followed['time']
            nickname = followed['nickname']
            playlistCount = followed['playlistCount']
            fan = {
                 'userId': userId, 
                 'avatar': avatar,
                 'vipType': vipType,
                 'gender': gender,
                 'eventCount': eventCount,
                 'followeds': fan_followeds,
                 'follows': fan_follows,
                 'signature': signature,
                 'time': time1,
                 'nickname': nickname,
                 'playlistCount': playlistCount
                 }
            params2, encSecKey2 = self._get_params2(userId)
            formdata2 = {
                       'params': params2, 'encSecKey': encSecKey2
                       }
            yield scrapy.FormRequest(url = self.post_url2, formdata = formdata2, meta = fan, callback = self.parse2)

    
    def parse2(self, response):
        json1 = json.loads(response.body)

        try:
            total_record_count = len(json1['allData'])
            week_record_count = len(json1['weekData'])
        except:
            total_record_count = 'secret'
            week_record_count = 'secret'

        avatar = response.meta['avatar']
        userId = response.meta['userId']
        vipType = response.meta['vipType']
        gender = response.meta['gender']
        eventCount = response.meta['eventCount']
        fan_followeds = response.meta['followeds']
        fan_follows = response.meta['follows']
        signature = response.meta['signature']
        time1 = response.meta['time']
        nickname = response.meta['nickname']
        playlistCount = response.meta['playlistCount']
        fans = {
                 'userId': userId, 
                 'avatar': avatar,
                 'vipType': vipType,
                 'gender': gender,
                 'eventCount': eventCount,
                 'followeds': fan_followeds,
                 'follows': fan_follows,
                 'signature': signature,
                 'time': time1,
                 'nickname': nickname,
                 'playlistCount': playlistCount,
                 'total_record_count': total_record_count,
                 'week_record_count': week_record_count
                                
                    }
        yield fans