# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:03:43 2019

@author: Administrator
"""

from selenium import webdriver
import time

def login(email, password):

    browser = webdriver.Chrome()
    browser.get("https://passport.csdn.net/login")
    time.sleep(1)
    #找到账号登陆接口并点击
    input_button = browser.find_element_by_xpath('//div[@class="main-select"]/ul/li[2]/a')
    input_button.click()
    time.sleep(1)
    # 输入账号密码，并点击登陆
    input_element = browser.find_element_by_xpath(
        '//div[@class="col-xs-12 col-sm-12 control-col-pos col-pr-no col-pl-no"]/input[@id="all"]')
    input_element.send_keys(email)
    time.sleep(1)
    # 输入密码
    input_password = browser.find_element_by_xpath(
        '//div[@class="col-xs-12 col-sm-12 control-col-pos col-pr-no col-pl-no"]/input[@id="password-number"]')
    input_password.send_keys(password)
    time.sleep(1)
    # 点击登陆
    touch_button = browser.find_element_by_xpath('//button')
    touch_button.click()


if __name__ == '__main__':
    
    email = input("请输入你的账号:")
    password = input("请输入你的密码:")
    login(email, password)