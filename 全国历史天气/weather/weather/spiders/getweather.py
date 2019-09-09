# -*- coding: utf-8 -*-
import scrapy


class GetweatherSpider(scrapy.Spider):
    name = 'getweather'
    start_urls = ['https://lishi.tianqi.com/']

    def parse(self, response):
        city_url=[]
        city_name=[]
        for alpha in [chr(i) for i in range(65,91)]:
            city_url.extend(response.xpath('//ul[@id="city_{}"]/li/a/@href'.format(alpha)).extract()[1:])
            city_name.extend(response.xpath('//ul[@id="city_{}"]/li/a/text()'.format(alpha)).extract()[1:])
        for j in range(len(city_url)):
            yield scrapy.Request(city_url[j],callback=self.parse_info1,meta={'city':city_name[j]})
        
    def parse_info1(self,response):
        
        detail_href=response.xpath('//div[@class="tqtongji1"]/ul/li/a/@href').extract()[:-24]
        print(detail_href)
        for href in detail_href:
            yield scrapy.Request(href,callback=self.parse_info2,meta=response.meta)
            
            
            
    def parse_info2(self,response):
        
        date=response.xpath('//div[@class="tqtongji2"]/ul/li[1]/a/text()').extract()
        high_temp=response.xpath('//div[@class="tqtongji2"]/ul/li[2]/text()').extract()[1:]
        low_temp=response.xpath('//div[@class="tqtongji2"]/ul/li[3]/text()').extract()[1:]
        weather=response.xpath('//div[@class="tqtongji2"]/ul/li[4]/text()').extract()[1:]
        wind_direct=response.xpath('//div[@class="tqtongji2"]/ul/li[5]/text()').extract()[1:]
        wind_power=response.xpath('//div[@class="tqtongji2"]/ul/li[6]/text()').extract()[1:]
            
        for i in range(len(date)):   
            yield {
            '城市': response.meta['city'],
            '日期': date[i],
            '最高气温': high_temp[i],
            '最低气温': low_temp[i],
            '天气情况': weather[i],
            '风向': wind_direct[i],
            '风力': wind_power[i],
             }