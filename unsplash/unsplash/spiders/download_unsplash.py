# -*- coding: utf-8 -*-
import scrapy
from unsplash.items import UnsplashItem
import json


class DownloadUnspalshSpider(scrapy.Spider):
    name = 'download_unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['http://unsplash.com/napi/photos?page={}&per_page=12'.format(n) for n in range(10224)]

    def parse(self,response):
        play_url = json.loads(response.text)
        for download_url in play_url:
            image_url=download_url['links']['download']
            yield scrapy.Request(image_url,callback=self.parse_url)
    
    def parse_url(self,response):
        pic=UnsplashItem()
        image=response.body
        pic['image']=image
        yield pic

        
