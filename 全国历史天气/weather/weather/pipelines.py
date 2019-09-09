# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient

 # 将爬取的内容保存到mongoDB中
class WeatherPipeline(object):

    def __init__(self):
        # 连接
        self.client = MongoClient()

        self.col = self.client['weather']
        self.info = self.col.info
        # 先清除之前保存的数据
        # self.ershoufang.delete_many({})

    def process_item(self, item, spider):
        self.info.insert_one(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()