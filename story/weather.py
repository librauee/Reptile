# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 13:11:58 2019

@author: Lee
"""


# import itchat 
import time
import requests
from lxml import etree
import wxpy

def getWeather():
    # 使用BeautifulSoup获取天气信息
    r=requests.get('https://tianqi.sogou.com/?tid=101280601')
    tree=etree.HTML(r.text)
    today=tree.xpath('//div[@class="row2 row2-1"]/a/text()')[0]
    weather=tree.xpath('//p[@class="des"]/text()')[1]
    wind=tree.xpath('//p[@class="wind"]/text()')[1]
    quality=tree.xpath('//span[@class="liv-text"]/a/em/text()')[0]
    rank=tree.xpath('//span[@class="liv-img liv-img-cor1"]/text()')[0]
    high=tree.xpath('//div[@class="r-temp"]/@data-high')[0].split(',')[1]
    low=tree.xpath('//div[@class="r-temp"]/@data-low')[0].split(',')[1]
    content='早上好，亲爱的！\n今日份的天气请注意查看喔~\n今天是：'+today+'\n天气：'+weather+'\n风级：'+wind+'\n最高温度:'+high+'\n最低温度:'+low+'\n空气质量指数:'+quality+' 等级：'+rank
    print(content)
    return content


def main():
    
    message = getWeather()
    print('成功获取天气信息')

#    # 参数hotReload=True实现保持微信网页版登陆状态，下次发送无需再次扫码
#    itchat.auto_login()
#    users=itchat.search_friends('')
#    print(users)
#    userName=users[0]['UserName']
#    ret=itchat.send(msg = message, toUserName = userName)
#    if ret:
#        print("成功发送")
#    else:
#        print("发送失败")
#    time.sleep(3)
#    itchat.logout()
    
    bot=wxpy.Bot()
    my_friend=bot.friends().search('Snall')[0]
    my_friend.send(message[0])




if __name__ == '__main__':
    main()
