# -*- coding: utf-8 -*-
import scrapy
import re

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock=re.findall(r'[s][hz]\d{6}',href)[0]
                url='https://gupiao.baidu.com/stock/'+stock+'.html'
                headers={'Accept':'*/*',
                         'Accept-Encoding':'gzip, deflate, br',
                         'Accept-Language':'zh-CN,zh;q=0.9',
                         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                         'Referer':'https://gupiao.baidu.com/'
                        }
                yield scrapy.Request(url,headers=headers,callback=self.parse_stock)
            except:
                continue
            
    def parse_stock(self,response):
        infoDict={}
        stockinfo=response.css('.stock-bets')
        name=stockinfo.css('.bets-name').extract()[0]
        keyList=stockinfo.css('dt').extract()
        valueList=stockinfo.css('dd').extract()
        for i in range(len(keyList)):
            key=re.findall(r'>.*</dt>',keyList[i])[0][1:-5]
            try:
                val=re.findall(r'\d+\.?.*</dd>',valueList[i])[0][0:-5]
            except:
                val='--'
            infoDict[key]=val
        infoDict.update({'股票名称':re.findall('\s.*\(',name)[0].split()[0]+re.findall('\>.*\<',name)[0][1:-1]})
        yield infoDict
        