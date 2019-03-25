# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:19:25 2019

@author: Administrator
"""

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
#browser.quit()
browser.current_url
browser.maximize_window()
ele=browser.find_element_by_id('kw')
id(ele)
ele.clear()
ele.send_keys("北京大学")
time.sleep(2)
ele.clear()
ele.send_keys("清华大学")

ele.send_keys(Keys.RETURN)

time.sleep(2)
browser.back()
browser.close()


