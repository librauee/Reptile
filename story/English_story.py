# -*- coding: utf-8 -*-
"""
Created on Sat May  4 19:02:32 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime
import time

def getDays():
    
    inlove_date=datetime.datetime(2017,8,31)
    today_date=datetime.datetime.today()
    inlove_days=(today_date-inlove_date).days
    return str(inlove_days)

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
    url='http://www.en8848.com.cn/'
    soup=BeautifulSoup(html,'html.parser')
    t=soup.find(attrs={'class':'ch_content'})
    #print(t)
    i=t.find_all('a')
    #print(i)
    for link in i[1:59:2]:
        urllist.append(url+link.get('href'))
        namelist.append(link.get('title'))


def parsehtml2(html):
    text=[]
    soup=BeautifulSoup(html,'html.parser')
    t=soup.find(attrs={'class':'jxa_content','id':'articlebody'})
    for i in t.findAll('p'):
        text.append(i.text)
    #print(text)
    return "\n".join(text)

def sendemail(url,headers,title):
    date_today=time.strftime("%Y-%m-%d", time.localtime())
    msg_from='870407139@qq.com'                                 #发送方邮箱
    passwd=''                                                   #填入发送方邮箱的授权码
    receivers=['870407139@qq.com']                              #收件人邮箱
                            
    subject="Today's story from Laofei " +str(date_today)       #主题     
    html=getHTMLText(url,headers)
    content='Dear Xiaofei:\n    We have been in love for '+getDays()+' Days !\n\n⭐⭐⭐⭐⭐❤❤💗❤❤⭐⭐⭐⭐⭐'+parsehtml2(html)                                        #正文
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
    for i in range(1,21):
        if i==1:
            url='http://www.en8848.com.cn/article/love/dating/index.html'
        else:
            url='http://www.en8848.com.cn/article/love/dating/index_'+str(i)+'.html'
        print ("正在爬取第%s页的英语短文链接：" % (i))
        print (url+'\n')
        html=getHTMLText(url,headers)
        parsehtml(namelist,urllist,html)
    print("爬取链接完成")
    date=int(getDays())-611
    sendemail(urllist[date],headers,namelist[date])
    
    
if __name__=='__main__':
    main()
