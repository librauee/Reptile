# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 18:24:17 2019

@author: Administrator
"""

import time
from selenium import webdriver
from fuzzywuzzy import process,fuzz

class Auto(object):
    
    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.browser.get('http://my.hfut.edu.cn/login.portal')
        self.username=username
        self.password=password
        
    def check_login(self):
        try:
            text=self.browser.find_element_by_xpath('//a[@title="实验室准入"]')
            print("您已经成功登录！")
            return True
        except:
            print("验证码错误！")
            return False
            
    

    
    
    
    def login(self):
    
        user_name=self.browser.find_element_by_id('username')
        pwd=self.browser.find_element_by_id('password')
        login_btn=self.browser.find_element_by_name('btn')   #登录按钮
        cap=self.browser.find_element_by_name('captcha')
        user_name.send_keys(self.username)              #输入用户名
        pwd.send_keys(self.password)                    #输入密码

        result=input("请输入验证码：")
        cap.send_keys(result)
        
        login_btn=self.browser.find_element_by_name('btn')#登陆按钮
        login_btn.send_keys("\n")       #点击登陆按钮
        time.sleep(5)
        flag=self.check_login()
        
        while not flag:
            self.login()

        
        
    def enter_article(self):

        lab=self.browser.find_element_by_xpath('//a[@title="实验室准入"]')
        lab.send_keys("\n")
        time.sleep(2)
        windows=self.browser.window_handles
        self.browser.switch_to.window(windows[-1])
        safe=self.browser.find_element_by_xpath('//li[@class="lx"]')
        safe.click()
        time.sleep(2)
        windows=self.browser.window_handles
        self.browser.switch_to.window(windows[-1])
        article=self.browser.find_element_by_xpath('//div[@class="lx"]/ul[@class="clearfix"]/li[1]/a')
        article.send_keys("\n")
        print("现在开始进行阅读……")
        time.sleep(2)
        for j in range(40):
            for i in range(1,11):
                self.choose(i)
            next_page=self.browser.find_element_by_xpath('//input[@type="button"][2]')
            next_page.click()
    
        submit=self.browser.find_element_by_xpath('//input[@type="button"][3]')
        submit.click()
        time.sleep(2)
        confirm=self.browser.switch_to_alert()
        print(confirm.text)
        confirm.accept()        
        
        
        
        
    def choose(self,i):
        
        question=self.browser.find_element_by_xpath('//div[@class="shiti"][{}]/h3'.format(i)).text
        print(question)
        
        a=process.extractOne(question, dic.keys())
        ans=dic[a[0]]
        if ans=='正确':
            ans_button_yes=self.browser.find_element_by_xpath('//div[@class="shiti"][{}]/ul[@class="xuanxiang_panduan"]/li[1]/input'.format(i))
            ans_button_yes.click()
        elif ans=='错误':
            ans_button_no=self.browser.find_element_by_xpath('//div[@class="shiti"][{}]/ul[@class="xuanxiang_panduan"]/li[2]/input'.format(i))
            ans_button_no.click()
        elif ans=='A':
            ans_button_A=self.browser.find_element_by_xpath(' //div[@class="shiti"][{}]/ul[@class="xuanxiang_xuanze"]/li[1]/label'.format(i))
            ans_button_A.click()
        elif ans=='B':
            ans_button_A=self.browser.find_element_by_xpath(' //div[@class="shiti"][{}]/ul[@class="xuanxiang_xuanze"]/li[2]/label'.format(i))
            ans_button_A.click()
        elif ans=='C':
            ans_button_A=self.browser.find_element_by_xpath(' //div[@class="shiti"][{}]/ul[@class="xuanxiang_xuanze"]/li[3]/label'.format(i))
            ans_button_A.click()
        else:
            ans_button_A=self.browser.find_element_by_xpath(' //div[@class="shiti"][{}]/ul[@class="xuanxiang_xuanze"]/li[4]/label'.format(i))
            ans_button_A.click()
            
                
                
                
                
if __name__=='__main__':
    
    dic={'因运动量过度产生的酸疼，可以通过减量、休息、按摩、热敷等方法来帮助机体积极恢复。':'正确','您已经成功登录！':'错误','进行危险物质、挥发性有机溶剂、特定化学物质或毒性化学物质等操作实验或研究，说法错误的是：':'A'}
    username=''
    password=''
    auto=Auto(username,password)
    auto.login()
    auto.enter_article()
