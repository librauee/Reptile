# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影标题
    title = scrapy.Field()
    # 豆瓣评分
    star = scrapy.Field()
    # 主演信息
    Staring = scrapy.Field()
    # 豆瓣排名
    rank = scrapy.Field()
    # 描述
    quote = scrapy.Field()
    # 豆瓣详情页
    url = scrapy.Field()
    # 电影海报图片url
    image_url = scrapy.Field()
    # 电影海报保存到本地的path
    save_path = scrapy.Field()
