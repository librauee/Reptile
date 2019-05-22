# -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:24:46 2019

@author: Administrator
"""

import requests
import re 
from lxml import etree


class Spyder_bus(object):
    
    def __init__(self):
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
                                     x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                                     Chrome/70.0.3538.102 Safari/537.36'}
        self.items=[]
        self.url='https://hangzhou.8684.cn/'
        
    def parse_navigation(self):
        r = requests.get(self.url, headers=self.headers)
        # 解析内容，获取所有导航链接
        tree = etree.HTML(r.text)
        number_href_list = tree.xpath('//div[@class="bus_kt_r1"]/a/@href')
        letter_href_list = tree.xpath('//div[@class="bus_kt_r2"]/a/@href')
        all_navigation=number_href_list + letter_href_list
        return all_navigation
    
    def parse_third_url(self,content):
        tree = etree.HTML(content)
        # 依次获取公交详细内容
        # 获取公交线路信息
        bus_number = tree.xpath('//div[@class="bus_i_t1"]/h1/text()')[0]
        bus_number = bus_number.replace('&nbsp', '')
        # 获取运行时间
        run_time = tree.xpath('//p[@class="bus_i_t4"][1]/text()')[0]
        run_time = re.sub(r'(.*?：)', '', run_time)
        # 获取票价信息
        ticket_info = tree.xpath('//p[@class="bus_i_t4"][2]/text()')[0]
        ticket_info = re.sub(r'(.*?：)', '', ticket_info)
        # 该公交线路公司名称
        company_info = tree.xpath('//p[@class="bus_i_t4"]/a/text()')[0]
        # 获取更新时间
        update_time = tree.xpath('//p[@class="bus_i_t4"][4]/text()')[0]
        update_time = re.sub(r'(.*?：)', '', update_time)

        total_list = tree.xpath('//span[@class="bus_line_no"]/text()')
        # 获取上行总站数
        up_total = total_list[0]
        # 将里面空格去掉
        up_total = up_total.replace('\xa0', '')
        # 获取上行所有站名
        up_site_list = tree.xpath('//div[@class="bus_line_site "][1]/div/div/a/text()')
        
        #有些线路只有单线，内环外环线路
        try:
        # 获取下行总站数
            down_total = total_list[1]
            down_total = down_total.replace('\xa0','')
        # 获取下行所有站名
            down_site_list = tree.xpath('//div[@class="bus_line_site "][2]/div/div/a/text()')
        # 将每一条公交线路存放到字典中
        except Exception as e:
            down_total = ''
            down_site_list = []

        item = {
                '线路名':   bus_number,
                '运行时间': run_time,
                '票价信息': ticket_info,
                '公司名称': company_info,
                '更新时间': update_time,
                '上行站数': up_total,
                '上行站点': up_site_list,
                '下行站数': down_total,
                '下行站点': down_site_list
                 }
        self.items.append(item)


    def parse_second_url(self,content):
        tree = etree.HTML(content)
        route_list = tree.xpath('//div[@id="con_site_1"]/a/@href')
        route_name = tree.xpath('//div[@id="con_site_1"]/a/text()')
        # 遍历上面的列表
        i = 0
        for route in route_list:
            print('开始爬取%s线路' % route_name[i])
            route = self.url + route
            r = requests.get(url=route, headers=self.headers)
            print('结束爬取%s线路' % route_name[i])
            # 解析内容，获取每一路公交的详细信息
            self.parse_third_url(r.text)
            i += 1


    def parse_first_url(self,navi_list):
            # 遍历列表，依次发送请求，解析内容，获取每个页面的所有公交线的url
        for url in navi_list:
            first_url =self.url + url
            print('开始爬取%s所有的公交信息' % first_url)
            r = requests.get(url=first_url, headers=self.headers)
            # 解析内容，获取每一路公交的详细的url
            self.parse_second_url(r.text)
            print('结束爬取%s所有的公交信息' % first_url)
            
    def save_to_txt(self):

        with open('hangzhou_bus_info.txt', 'w', encoding='utf-8') as f:
            for item in self.items:
                f.write(str(item)+'\n')
    


if __name__ == '__main__':
    
    bus_info=Spyder_bus()
    navigation=bus_info.parse_navigation()
    #print(navigation)
    bus_info.parse_first_url(navigation)
    bus_info.save_to_txt()





        
