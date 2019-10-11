# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:21:44 2019

@author: Lee
"""

import requests
import re
import tesserocr
from PIL import Image
from io import BytesIO

#
#url='http://syszr.hfut.edu.cn/redir.php'
#
#headers={
#        
#'Cookie': '',
#'Host': 'syszr.hfut.edu.cn',
#'Referer': 'http://syszr.hfut.edu.cn/redir.php?catalog_id=121&object_id=2731',
#'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
#        
#        }
#
#params={
#        'catalog_id': 121,
#        'object_id': 2729
#        }
#while 1:
#    r=requests.get(url,headers=headers,params=params)
#    r.encoding=r.apparent_encoding
#    t=re.findall(r'您的在线时长(.*?)秒',r.text)
#    print(t)
from selenium import webdriver


browser=webdriver.Chrome()
browser.get('http://my.hfut.edu.cn/login.portal')


def get_captcha():
    captcha=requests.get("http://my.hfut.edu.cn/captchaGenerate.portal", stream = True).content
    with open("captcha.jpg", "wb") as f:
        f.write(captcha)

def get_screenshot():
        
    screenshot=browser.get_screenshot_as_png()
    return Image.open(BytesIO(screenshot))

def get_geetest_image():
    #location=browser.find_element_by_xpath("//img[@id='captchaImg']")
#    a=browser.find_element_by_id('captchaImg')
#    location=a.location 
#    
#    size=a.size
#    print(location['x'])
#    
#    bottom,top,left,right=location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
#    print("验证图片位置",bottom,top,left,right)
    bottom,top,left,right=287,307,920,974
    screenshot=get_screenshot().convert('RGB')
    captcha_img=screenshot.crop((left,bottom,right,top))
    captcha_img.save('captcha.jpg')


def ocr():

    image=Image.open('captcha.jpg')
    image=image.convert('L')
    threshold=127
    table=[]
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
    print(table)   
    image=image.point(table,'1')
    result=tesserocr.image_to_text(image)
    print(result)
    return result


def login(number,password):
    user_name=browser.find_element_by_id('username')
    pwd=browser.find_element_by_id('password')
    
    cap=browser.find_element_by_name('captcha')
    get_geetest_image()
    user_name.send_keys(number)#输入手机号码
    pwd.send_keys(password)#输入密码

    result=ocr()
    cap.send_keys(result)
    login_btn=browser.find_element_by_name('btn')#登陆按钮
    login_btn.click()#点击登陆按钮
    
    time.sleep(5)
    current=browser.current_window_handle#当前页面的句柄
    lab=browser.find_element_by_xpath('//a[@title="实验室准入"]')
    lab.click()
    time.sleep(1)
    handles=browser.window_handles
    for handle in handles:
        if handle!=current:
            browser.switch_to_window(handle)

    
login('','')
    

