# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WyyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    avatar = scrapy.Field()
    userId = scrapy.Field()
    # vipRights = scrapy.Field()
    vipType =scrapy.Field()
    gender = scrapy.Field()
    eventCount = scrapy.Field()
    fan_followeds = scrapy.Field()
    fan_follows = scrapy.Field()
    signature = scrapy.Field()
    time = scrapy.Field()
    nickname = scrapy.Field()
    playlistCount = scrapy.Field()
    total_record_count = scrapy.Field()
    week_record_count = scrapy.Field()