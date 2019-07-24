# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:56:26 2019

@author: Lee
"""

# -*- coding: utf-8 -*-
import scrapy


class Lianjiacrawl2Spider(scrapy.Spider):
    name = 'lianjiacrawl2'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hz.lianjia.com/zufang/pg{}/'.format(i) for i in range(1,101)]

    def parse(self, response):
        urls = response.xpath('//p[@class="content__list--item--title twoline"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request('https://hz.lianjia.com'+url,callback=self.parse_info)
    
    def parse_info(self,response):
        title = response.xpath('//p[@class="content__title"]/text()').extract_first()
        price = response.xpath('string(//p[@class="content__aside--title"])').extract_first()


        base1 = response.xpath('//div[@class="content__article__info"]/ul')
        time = base1.xpath('./li[2]/text()').extract_first().split("：" )[1]
        ru_zhu = base1.xpath('./li[3]/text()').extract_first().split("：" )[1]
        zu_qi = base1.xpath('./li[5]/text()').extract_first().split("：" )[1]
        kan_fang = base1.xpath('./li[6]/text()').extract_first().split("：" )[1]
        floor = base1.xpath('./li[8]/text()').extract_first().split("：" )[1]
        lift = base1.xpath('./li[9]/text()').extract_first().split("：" )[1]
        car = base1.xpath('./li[11]/text()').extract_first().split("：" )[1]
        water = base1.xpath('./li[12]/text()').extract_first().split("：" )[1]
        electric = base1.xpath('./li[14]/text()').extract_first().split("：" )[1]
        gas = base1.xpath('./li[15]/text()').extract_first().split("：" )[1]
        warm = base1.xpath('./li[17]/text()').extract_first().split("：" )[1]
        
        base2 = response.xpath('//p[@class="content__article__table"]')
        house = base2.xpath('./span[1]/text()').extract_first()
        architecture = base2.xpath('./span[2]/text()').extract_first()
        area = base2.xpath('./span[3]/text()').extract_first()
        orientation = base2.xpath('./span[4]/text()').extract_first()
        
        if response.xpath('//li[@class="fl oneline television_no "]'):
            television = '无'
        else:
            television = '有'
            
        if response.xpath('//li[@class="fl oneline refrigerator_no "]'):
            refrigerator = '无'
        else:
            refrigerator = '有'
            
        if response.xpath('//li[@class="fl oneline washing_machine_no "]'):
            washing_machine = '无'
        else:
            washing_machine = '有'
            
        if response.xpath('//li[@class="fl oneline air_conditioner_no "]'):
            air_conditioner = '无'
        else:
            air_conditioner = '有'
            
        if response.xpath('//li[@class="fl oneline water_heater_no "]'):
            water_heater = '无'
        else:
            water_heater = '有'
            
        if response.xpath('//li[@class="fl oneline bed_no "]'):
            bed = '无'
        else:
            bed = '有'
            
        if response.xpath('//li[@class="fl oneline heating_no "]'):
            heating = '无'
        else:
            heating = '有'
            
        if response.xpath('//li[@class="fl oneline wifi_no "]'):
            wifi = '无'
        else:
            wifi = '有'
        
        if response.xpath('//li[@class="fl oneline wardrobe_no "]'):
            wardrobe = '无'
        else:
            wardrobe = '有'
        
        if response.xpath('//li[@class="fl oneline natural_gas_no "]'):
            natural_gas = '无'
        else:
            natural_gas = '有'

        yield {
            '名称': title,
            '价格': price,
            '发布时间': time,
            '方式': house,
            '户型': architecture,
            '面积': area,
            '朝向': orientation,
            '入住': ru_zhu,
            '租期': zu_qi,
            '看房': kan_fang,
            '楼层': floor,
            '电梯': lift,
            '车位': car,
            '用水': water,
            '用电': electric,
            '燃气': gas,
            '采暖': warm,
            '电视': television,
            '冰箱': refrigerator,
            '洗衣机': washing_machine,
            '空调': air_conditioner,
            '热水器': water_heater,
            '床': bed,
            '暖气': heating,
            '宽带': wifi,
            '衣柜': wardrobe,
            '天然气': natural_gas,
            

             }