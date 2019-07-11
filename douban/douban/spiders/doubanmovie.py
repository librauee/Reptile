# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    start_urls = ['https://movie.douban.com/top250']
    # 如果有多个spider, 则通过custom_settings配置, 取代全局settings文件中的部分
    # 注意SaveImagePipeline的优先级应该要高于Save2MongoPipeline的优先级, 因为将电影海报保存到本地后, item还需要记录保存到本地的路径
    custom_settings = {
        'ITEM_PIPELINES': {
            'douban.pipelines.SaveImgPipeline': 100,
            'douban.pipelines.Save2MongoPipeline': 200,
        },
    }
    def parse(self, response):
        for item in response.css('.item'):
            movie = DoubanItem()
            #Staring = item.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()').extract_first()
            Staring =item.css('.bd p::text').extract_first()
            rank = item.css('.pic em::text').extract_first()
            title = item.css('.hd span.title::text').extract_first()
            star = item.css('.star span.rating_num::text').extract_first()
            quote = item.css('.quote span.inq::text').extract_first()
            url = item.css('.pic a::attr("href")').extract_first()
            image_url = item.css('.pic img::attr("src")').extract_first()
            movie['rank'] = rank
            movie['title'] = title
            movie['star'] = star
            movie['Staring'] = Staring
            movie['quote'] = quote
            movie['url'] = url
            movie['image_url'] = image_url
            yield movie
    
        # 获取下一页的url
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)

