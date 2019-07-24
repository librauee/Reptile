# -*- coding: utf-8 -*-
import scrapy


class LianjiacrawlSpider(scrapy.Spider):
    name = 'lianjiacrawl'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hz.lianjia.com/ershoufang/pg{}/'.format(i) for i in range(1,101)]

    def parse(self, response):
        urls = response.xpath('//div[@class="info clear"]/div[@class="title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_info)
    
    def parse_info(self,response):
        total_price = response.xpath('concat(//span[@class="total"]/text(),//span[@class="unit"]/span/text())').extract_first()
        unit_price = response.xpath('string(//span[@class="unitPriceValue"])').extract_first()
        residential_district = response.xpath('//a[contains(@class,"info")]/text()').extract_first()
        district = response.xpath('string(//div[@class="areaName"]/span[@class="info"])').extract_first()

        base1 = response.xpath('//div[@class="base"]//ul')
        apartment = base1.xpath('./li[1]/text()').extract_first()
        floor = base1.xpath('./li[2]/text()').extract_first()
        area = base1.xpath('./li[3]/text()').extract_first()
        architecture =base1.xpath('./li[4]/text()').extract_first()
        orientation = base1.xpath('./li[7]/text()').extract_first()
        renovation = base1.xpath('./li[9]/text()').extract_first()
        tihu_ration = base1.xpath('./li[last()-2]/text()').extract_first()
        property_right_year = base1.xpath('./li[last()]/text()').extract_first()

        base2 = response.xpath('//div[@class="transaction"]//ul')
        purpose = base2.xpath('./li[4]/span[2]/text()').extract_first()
        property_right = base2.xpath('./li[6]/span[2]/text()').extract_first()

        yield {
            '总价': total_price,
            '单价': unit_price,
            '小区': residential_district,
            '区域': district,
            '户型': apartment,
            '楼层': floor,
            '面积': area,
            '户型结构': architecture,
            '朝向': orientation,
            '装修情况': renovation,
            '梯户比例': tihu_ration,
            '产权年限': property_right_year,
            '用途': purpose,
            '产权所属': property_right,
             }

