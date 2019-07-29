# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class WyyPipeline(object):
    
    def __init__(self) -> None:
        # 连接
        self.client = MongoClient(host='localhost', port=27017)
        # 如果设置有权限, 则需要先登录
        # db_auth = self.client.admin
        # db_auth.authenticate('root', 'root')
        # 需要保存到的collection
        self.col = self.client['wyy']
        self.fans = self.col.fans2


    def process_item(self, item, spider):
        res = dict(item)
        self.fans.update_one({"userId":res['userId']}, {"$set": res}, upsert = True)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

