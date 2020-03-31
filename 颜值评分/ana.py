# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 23:10:54 2019

@author: Administrator
"""

from pymongo import MongoClient
import pandas as pd
import os
from PIL import Image
import math
import requests
from wordcloud import WordCloud
import jieba




"""
问题词云
"""

wordlist=["你见过最漂亮的女生长什么样？","你见过的有些人能漂亮到什么程度？","平常人可以漂亮到什么程度？","你见过最美的高中女生是什么样子？","你见过的最美的女性照片是哪张？","帅得惨绝人寰是帅到了哪种程度？","你见过最帅的人是什么样的？","你见过最帅的高中男生长什么样？"]
text="".join(wordlist)
wordlist=jieba.cut(text,cut_all=False)
wl=" ".join(wordlist)
#设置词云
wc=WordCloud(
               background_color = "white", #设置背景颜色
               mask = plt.imread('zhihu.png'),  #设置背景图片
               stopwords = ["的", "这种", "这样", "还是", "就是", "这个"], #设置停用词
               font_path = "C:\Windows\Fonts\simkai.ttf",  # 设置为楷体 常规
               max_words=300,
               max_font_size=50,
               min_font_size=8,
               random_state=50,
               
    )
myword=wc.generate(wl)#生成词云
wc.to_file('result.jpg')



# 显示所有列
pd.options.display.max_columns=None 
# 显示所有行
# pd.options.display.max_rows=None
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

#数据预处理
db=MongoClient().beauty
data=pd.DataFrame(list(db['score9'].find()))
data.drop('_id',axis=1,inplace=True)

#评分均值
avg_score=[]
for i in range(10):
    data=pd.DataFrame(list(db['score{}'.format(i+1)].find()))
    data.drop('_id',axis=1,inplace=True)
    score=data['score'].sum()/len(data)
    avg_score.append(score)

print(sum(avg_score)/len(avg_score))


"""
单个问题最高最低评分
"""
print(data['score'].sum()/len(data))

print(data.max())
print(data.min())
data.sort_values('score',inplace=True)
print(data)


"""
女性集合
"""


data6=pd.DataFrame(list(db['score6'].find()))
data6.drop('_id',axis=1,inplace=True)

data7=pd.DataFrame(list(db['score7'].find()))
data7.drop('_id',axis=1,inplace=True)

data8=pd.DataFrame(list(db['score8'].find()))
data8.drop('_id',axis=1,inplace=True)

data9=pd.DataFrame(list(db['score9'].find()))
data9.drop('_id',axis=1,inplace=True)

data10=pd.DataFrame(list(db['score10'].find()))
data10.drop('_id',axis=1,inplace=True)

woman_data=pd.concat([data6,data7,data8,data9,data10])
woman_data.sort_values('score',inplace=True)

high_woman=woman_data[woman_data['score']>91]
print(high_woman)


"""
图片下载
"""
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
url=list(high_woman['image_url'])
print(url)
for i in range(len(url)):
    r=requests.get(url[i],headers=headers)
    with open('pic_girl/'+url[i][-15:],'wb') as f:
        f.write(r.content)


"""
图片合成
"""

def compose(img_dir):
    
    img_list=[img_dir+img_name for img_name in os.listdir(img_dir)]
    size=3000
    rows=int(math.sqrt(len(img_list)))
    each_size=int(size/rows)
    img=Image.new('RGB',(each_size*rows,each_size*rows))
    x=y=0
    for pic in img_list:
        pic=Image.open(pic)
        pic=pic.resize((each_size,each_size))
        img.paste(pic,(x*each_size,y*each_size))
        x+=1
        if x==rows:
            x=0
            y+=1
    img.save("new.jpg")
    
compose('pic_girl/')



"""
男性集合
"""
data1=pd.DataFrame(list(db['score1'].find()))
data1.drop('_id',axis=1,inplace=True)

data2=pd.DataFrame(list(db['score2'].find()))
data2.drop('_id',axis=1,inplace=True)

data3=pd.DataFrame(list(db['score3'].find()))
data3.drop('_id',axis=1,inplace=True)

data4=pd.DataFrame(list(db['score4'].find()))
data4.drop('_id',axis=1,inplace=True)

data5=pd.DataFrame(list(db['score5'].find()))
data5.drop('_id',axis=1,inplace=True)

man_data=pd.concat([data1,data2,data3,data5,data4])
man_data.sort_values('score',inplace=True)
print(man_data)
high_man=man_data[man_data['score']>91]

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
url=list(high_man['image_url'])
print(url)
for i in range(len(url)):
    r=requests.get(url[i],headers=headers)
    with open('pic_boy/'+url[i][-15:],'wb') as f:
        f.write(r.content)