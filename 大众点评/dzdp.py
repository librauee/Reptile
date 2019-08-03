# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:42:27 2019

@author: Lee
"""

from fontTools.ttLib import TTFont
import requests
import re
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from pandas.io.json import json_normalize
import random


def decrypt_font(url,response):
    '''
    输入：链接和html信息
    输出：返回解决字体反爬后的页面源码
    
    '''
    headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
             }
    font1=TTFont('a.woff')
    base_font=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '店', '中', '美', '家', '馆', '小', '车', '大', '市', '公', '酒', '行', '国', '品', '发', '电', '金', '心', '业', '商', '司', '超', '生', '装', '园', '场', '食', '有', '新', '限', '天', '面', '工', '服', '海', '华', '水', '房', '饰', '城', '乐', '汽', '香', '部', '利', '子', '老', '艺', '花', '专', '东', '肉', '菜', '学', '福', '饭', '人', '百', '餐', '茶', '务', '通', '味', '所', '山', '区', '门', '药', '银', '农', '龙', '停', '尚', '安', '广', '鑫', '一', '容', '动', '南', '具', '源', '兴', '鲜', '记', '时', '机', '烤', '文', '康', '信', '果', '阳', '理', '锅', '宝', '达', '地', '儿', '衣', '特', '产', '西', '批', '坊', '州', '牛', '佳', '化', '五', '米', '修', '爱', '北', '养', '卖', '建', '材', '三', '会', '鸡', '室', '红', '站', '德', '王', '光', '名', '丽', '油', '院', '堂', '烧', '江', '社', '合', '星', '货', '型', '村', '自', '科', '快', '便', '日', '民', '营', '和', '活', '童', '明', '器', '烟', '育', '宾', '精', '屋', '经', '居', '庄', '石', '顺', '林', '尔', '县', '手', '厅', '销', '用', '好', '客', '火', '雅', '盛', '体', '旅', '之', '鞋', '辣', '作', '粉', '包', '楼', '校', '鱼', '平', '彩', '上', '吧', '保', '永', '万', '物', '教', '吃', '设', '医', '正', '造', '丰', '健', '点', '汤', '网', '庆', '技', '斯', '洗', '料', '配', '汇', '木', '缘', '加', '麻', '联', '卫', '川', '泰', '色', '世', '方', '寓', '风', '幼', '羊', '烫', '来', '高', '厂', '兰', '阿', '贝', '皮', '全', '女', '拉', '成', '云', '维', '贸', '道', '术', '运', '都', '口', '博', '河', '瑞', '宏', '京', '际', '路', '祥', '青', '镇', '厨', '培', '力', '惠', '连', '马', '鸿', '钢', '训', '影', '甲', '助', '窗', '布', '富', '牌', '头', '四', '多', '妆', '吉', '苑', '沙', '恒', '隆', '春', '干', '饼', '氏', '里', '二', '管', '诚', '制', '售', '嘉', '长', '轩', '杂', '副', '清', '计', '黄', '讯', '太', '鸭', '号', '街', '交', '与', '叉', '附', '近', '层', '旁', '对', '巷', '栋', '环', '省', '桥', '湖', '段', '乡', '厦', '府', '铺', '内', '侧', '元', '购', '前', '幢', '滨', '处', '向', '座', '下', '県', '凤', '港', '开', '关', '景', '泉', '塘', '放', '昌', '线', '湾', '政', '步', '宁', '解', '白', '田', '町', '溪', '十', '八', '古', '双', '胜', '本', '单', '同', '九', '迎', '第', '台', '玉', '锦', '底', '后', '七', '斜', '期', '武', '岭', '松', '角', '纪', '朝', '峰', '六', '振', '珠', '局', '岗', '洲', '横', '边', '济', '井', '办', '汉', '代', '临', '弄', '团', '外', '塔', '杨', '铁', '浦', '字', '年', '岛', '陵', '原', '梅', '进', '荣', '友', '虹', '央', '桂', '沿', '事', '津', '凯', '莲', '丁', '秀', '柳', '集', '紫', '旗', '张', '谷', '的', '是', '不', '了', '很', '还', '个', '也', '这', '我', '就', '在', '以', '可', '到', '错', '没', '去', '过', '感', '次', '要', '比', '觉', '看', '得', '说', '常', '真', '们', '但', '最', '喜', '哈', '么', '别', '位', '能', '较', '境', '非', '为', '欢', '然', '他', '挺', '着', '价', '那', '意', '种', '想', '出', '员', '两', '推', '做', '排', '实', '分', '间', '甜', '度', '起', '满', '给', '热', '完', '格', '荐', '喝', '等', '其', '再', '几', '只', '现', '朋', '候', '样', '直', '而', '买', '于', '般', '豆', '量', '选', '奶', '打', '每', '评', '少', '算', '又', '因', '情', '找', '些', '份', '置', '适', '什', '蛋', '师', '气', '你', '姐', '棒', '试', '总', '定', '啊', '足', '级', '整', '带', '虾', '如', '态', '且', '尝', '主', '话', '强', '当', '更', '板', '知', '己', '无', '酸', '让', '入', '啦', '式', '笑', '赞', '片', '酱', '差', '像', '提', '队', '走', '嫩', '才', '刚', '午', '接', '重', '串', '回', '晚', '微', '周', '值', '费', '性', '桌', '拍', '跟', '块', '调', '糕']
    base_uniname=font1['cmap'].tables[0].ttFont.getGlyphOrder()[2:]
    # 使用百度的FontEditor找到本地字体文件name和数字之间的对应关系, 保存到字典中
    base_dict=dict(zip(base_uniname,base_font))
    name_list1=font1.getGlyphNames()[1:-1]    
    text=requests.get(url,headers=headers).text
    # 正则匹配字体woff文件
    font_files=get_woffs(text)       
    for i in range(len(font_files)):
        if os.path.exists(font_files[i][-13:]):
            pass
        else:
            new_file=requests.get('http://'+font_files[i],headers)
            with open(font_files[i][-13:],'wb') as f:
                f.write(new_file.content)
        font2=TTFont(font_files[i][-13:])
        # font2.saveXML('font_{}.xml'.format(i))
        name_list2=font2.getGlyphNames()[1:-1]
        # 构造新映射
        new_dict={}
        for name2 in name_list2:
            obj2=font2['glyf'][name2]
            for name1 in name_list1:
                obj1=font1['glyf'][name1]
                # 对象相等则说明对应的数字相同​
                if obj1==obj2:
                    new_dict[name2]=base_dict[name1]
    
        for i in name_list2:
            pattern='&#x'+i[3:].lower()+';'
            response=re.sub(pattern,new_dict[i],response)
    return response


def get_woffs(text):

    woffs=[]
    urls=re.findall(r'url\("//(.*?)"\)', text)
    for url in urls:
        if url not in woffs and '.woff' in url:
            woffs.append(url)
    return woffs

def getshopurls():
    
    base_url='https://www.dianping.com/hangzhou/ch0/r1669p{}'
    headers={
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
         "Cookie": "_lxsdk_cuid=16bde7530eec8-0e10824e8c8703-e343166-15f900-16bde7530eec8; _lxsdk=16bde7530eec8-0e10824e8c8703-e343166-15f900-16bde7530eec8; _hc.v=0b99278f-49da-9814-a0fb-f22aeaf105fd.1562805351; cy=3; cye=hangzhou; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16c4733c2c4-52c-0a9-5a4%7C%7C69",
         "Host": "www.dianping.com",
         "Referer": "https://www.dianping.com/hangzhou/food"
    }
    urls=[]
    for i in range(1,51):
        r=requests.get(base_url.format(i),headers=headers)
        soup=BeautifulSoup(r.text,'html.parser')
        for shop in soup.find_all('div',attrs={'class':'pic'}):
            url=shop.find('a').get('href')
            urls.append(url)
    return urls

def getproxy():
    
    conn=MongoClient('127.0.0.1', 27017)
    db=conn.proxy
    mongo_proxy=db.good_proxy
    proxy_data=mongo_proxy.find()
    proxy=json_normalize([ip for ip in proxy_data])
    proxy_list=list(proxy['ip'])
    return proxy_list


if __name__ == '__main__':
    
    headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
             "Cookie": "_lxsdk_cuid=16bde7530eec8-0e10824e8c8703-e343166-15f900-16bde7530eec8; _lxsdk=16bde7530eec8-0e10824e8c8703-e343166-15f900-16bde7530eec8; _hc.v=0b99278f-49da-9814-a0fb-f22aeaf105fd.1562805351; cy=3; cye=hangzhou; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; thirdtoken=6de5fbfc-c0a1-447d-af09-47ad938b78a7; _lxsdk_s=16c47c94124-5c3-6b2-199%7C%7C1",
             "Host": "www.dianping.com"
             }
    # url='http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/5f0bd180c866836808810b429f404c48.css'
    proxy_list=getproxy()
    shopurls=getshopurls()

    # shopurls=['http://www.dianping.com/shop/8301189']
    for shopurl in shopurls:
        proxy=random.choice(proxy_list)
        response=requests.get(shopurl,headers=headers,proxies={'https': 'https://{}'.format(proxy),'http': 'http://{}'.format(proxy)}).text
        cssurl=re.findall(r'<link rel="stylesheet" type="text/css" href="(\/\/s3plus\.meituan\.net.*?\.css)">',response)[0]
        r=decrypt_font('https:'+cssurl,response)
        # print(r)
        comments=re.findall(r'<p class="desc J-desc">(.*?)</p>',r)
        # print(comments)
        for comment in comments:

            comment=comment.replace('<svgmtsi class="review">','')
            b=comment.replace('</svgmtsi>','').replace('<br />','')
            print(b)

