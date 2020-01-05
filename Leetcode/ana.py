# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:54:36 2020

@author: Lee
"""

from pymongo import MongoClient
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo,Line,WordCloud,Pie,Parallel,PictorialBar,Bar,Polar
from pyecharts.globals import ChartType, SymbolType


pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
db=MongoClient().leetcode
data=pd.DataFrame(list(db['2'].find()))
data=data.drop(columns='_id',axis=0)





data['acRate']=data['acRate'].apply(lambda x:float(x[:-1]))
# 最多喜欢
like=data.sort_values(by="likes",ascending=False)
print(like)
bar1=(
        Bar()
        .add_xaxis(list(like['title'])[:10])
        .add_yaxis("", list(like['likes'])[:10], category_gap="50%")
        .set_global_opts(title_opts=opts.TitleOpts(title="Leetcode点赞最多的十道题"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15,font_weight='bold')))
    )
bar1.render('Leetcode点赞最多的十道题.html')
# 最高ac率
print(data.sort_values(by="acRate",ascending=False))

# 最多提交
print(data.sort_values(by="totalSubmissionRaw",ascending=False))

# 难度分类
data_diff=data.groupby('difficulty').mean()
print(data_diff)

data_diff=data.groupby('difficulty').count()
print(data_diff)

data_diff=data.groupby('difficulty')
for a,b in data_diff:
    print(b.sort_values(by="likes",ascending=False))
    print(b.sort_values(by="acRate",ascending=False))
    print(b.sort_values(by="totalSubmissionRaw",ascending=False))