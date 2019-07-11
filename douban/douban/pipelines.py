# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import requests
from pymongo import MongoClient
from douban.settings import IMAGES_STORE

# 将爬取的内容保存到文件中
class SaveFilePipeline(object):

    def __init__(self) -> None:
        self.res_list = []
        super().__init__()

    def process_item(self, item, spider):
        res = dict(item)
        # print(str)
        self.res_list.append(res)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # print(self.res_list)
        # 打开文件, w+ 读写, 如果文件不存在会被创建, 存在则内容会被清空会重写写入
        file = codecs.open(filename="douban_movie_top_250.json", mode='w+', encoding='utf-8')
        # ensure_ascii=False 保证输出的是中文而不是unicode字符
        file.write(json.dumps(self.res_list, ensure_ascii=False))
        file.close()


# 保存电影海报图片
class SaveImgPipeline(object):

    def process_item(self, item, spider):
        file_path = "{}//{}_{}.jpg".format(IMAGES_STORE, item['rank'], item['title'])

        if os.path.exists(file_path):
            pass
        else:
            print("图片将保存到 ==> " + file_path)
            with open(file_path, "wb") as f:
                r = requests.get(item['image_url'])
                f.write(r.content)
        item['save_path'] = file_path
        return item


# 将爬取的内容保存到mongoDB中
class Save2MongoPipeline(object):

    def __init__(self) -> None:
        # 连接
        self.client = MongoClient(host='localhost', port=27017)
        # 如果设置有权限, 则需要先登录
        # db_auth = self.client.admin
        # db_auth.authenticate('root', 'root')
        # 需要保存到的collection
        self.col = self.client['douban_movie']
        self.top250 = self.col.top250
        # 先清除之前保存的数据
        # self.top250.delete_many({})

    def process_item(self, item, spider):
        res = dict(item)
        self.top250.insert_one(res)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()
