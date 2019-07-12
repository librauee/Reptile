# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from hashlib import md5

class UnsplashPipeline(object):
    def process_item(self, item, spider):
        r=item['image']  
        name=md5(r).hexdigest()
        file_path="F://pic//{}.jpg".format(name)
        if os.path.exists(file_path):
            pass
        else:
            with open(file_path,"wb") as f:
                f.write(r)
    


