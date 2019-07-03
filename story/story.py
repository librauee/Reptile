# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:25:45 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import random


def getHTMLText(url,headers):
    try:
        r=requests.get(url,headers=headers,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        #print(r.text)
        return r.text
       
    except:
        return "爬取失败"
    
def parsehtml(namelist,urllist,html):
    url='http://www.tom61.com/'
    soup=BeautifulSoup(html,'html.parser')
    t=soup.find('dl',attrs={'class':'txt_box'})
    #print(t)
    i=t.find_all('a')
    #print(i)
    for link in i:
        urllist.append(url+link.get('href'))
        namelist.append(link.get('title'))


def parsehtml2(html):
    text=[]
    soup=BeautifulSoup(html,'html.parser')
    t=soup.find('div',class_='t_news_txt')
    for i in t.findAll('p'):
        text.append(i.text)
    #print(text)
    return "\n".join(text)

def sendemail(url,headers):

    msg_from=''                                 #发送方邮箱
    passwd=''                                   #填入发送方邮箱的授权码
    receivers=[',']                             #收件人邮箱
                            
    subject='今日份的睡前小故事'                                     #主题     
    html=getHTMLText(url,headers)
    content=parsehtml2(html)                                        #正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        s=smtplib.SMTP_SSL("smtp.qq.com",465)                   #邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
    finally:
        s.quit()
        
def main():


    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
               }

    urllist=[]
    namelist=[]
    for i in range(1,11):
        if i==1:
            url='http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url='http://www.tom61.com/ertongwenxue/shuiqiangushi/index_'+str(i)+'.html'
        print ("正在爬取第%s页的故事链接：" % (i))
        print (url+'\n')
        html=getHTMLText(url,headers)
        parsehtml(namelist,urllist,html)
    print("爬取链接完成")
    '''
    for i in urllist:
        html=getHTMLText(i,headers)
        parsehtml2(html)
    '''
    sendemail(random.choice(urllist),headers)
if __name__=='__main__':
    main()
