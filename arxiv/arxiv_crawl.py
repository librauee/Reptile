from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def get_paper_info_list(number=20):
    """
    获取最新论文信息，并将信息汇总到csv文件
    """
    print("start scrapying……")
    url='https://arxiv.org/list/cs/pastweek?show={}'.format(number)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,'html.parser')
    dl=soup.dl
    date=soup.find('h3')
    identifier=dl.find_all('a',title='Download PDF')
    paper_pdf_list=['https://arxiv.org'+i['href'] for i in identifier]
    paper_title_list=dl.find_all('div', attrs={'class':'list-title mathjax'})
    paper_authors_list=dl.find_all('div', attrs={'class':'list-authors'})
    paper_subjects_list_raw=dl.find_all('div',attrs={'class':'list-subjects'})
    paper_subjects_list=[]
    for paper_subjects in paper_subjects_list_raw:
        subjects=paper_subjects.text.split(':')[1].strip(" ").strip("\n")
        subjects=subjects.split('; ')
        paper_subjects_list.append(subjects)

    items=[]
    for _,paper_info in enumerate(zip(paper_pdf_list,paper_title_list,paper_authors_list, paper_subjects_list)):
        # print(paper_info)
        items.append([paper_info[0],paper_info[1].text.split(':')[1].strip(" ").replace("\n",""),paper_info[2].text.split(':')[1].strip(" ").replace("\n",""),paper_info[3][0]])
    df=pd.DataFrame(index=list(range(1,len(items)+1)),columns=['文章下载链接','文章标题','文章作者','文章类别'],data=items)
    df.to_csv('arxiv_daily/'+date.text+'.csv')
    print("Generate summary Excel successfully!")
    return items,date.text


def select_paper_by_title(keywords):
    """
    搜索题目中带有指定关键词的论文
    """
    target_paper_list=[]
    for item in items:
        for keyword in keywords:
            if keyword in item[1]:
                target_paper_list.append(item)
                break

    return target_paper_list


def select_paper_by_subject(subject):
    """
    搜索相关主题的论文
    """
    target_paper_list=[]
    for item in items:
        if subject in item[3]:
            target_paper_list.append(item)

    return target_paper_list

def select_paper_mix(keywords,subject):
    """
    搜索相关主题并包含相应关键词的论文
    """
    target_paper_list=[]
    for item in items:
        if subject in item[3]:
            for keyword in keywords:
                if keyword in item[1]:
                    target_paper_list.append(item)
                    break
    return target_paper_list



def download(target_paper_list):
    """
    下载目标论文到本地
    """
    print("Downloading new paper ing....")
    temp_paper_list=[]
    for i in target_paper_list:
        if os.path.exists('arxiv_paper/{}.pdf'.format(i[1])):
            pass
        else:
            r=requests.get(i[0])
            with open ('arxiv_paper/{}.pdf'.format(i[1]),'wb') as f:
                f.write(r.content)
            print("finish downloading {}".format(i[1]))
            temp_paper_list.append(i[1])
            time.sleep(2)
    return temp_paper_list



def add_apart(m,apart_file):
    """
    添加邮件附件
    """
    Apart=MIMEApplication(open('arxiv_paper/'+apart_file, 'rb').read())
    Apart.add_header('Content-Disposition', 'attachment', filename=apart_file)
    m.attach(Apart)


def send_email(temp_paper_list,date):
    """
    邮件发送
    """
    today=time.strftime("%Y-%m-%d")
    print('start sending E-mail……')
    from_address=''                                     # 发邮件的邮箱地址
    password=''                                         # 邮箱授权码
    to_address=''                                       # 收邮件的邮箱地址

    content="Please check today's csv file which contains new paper on arxiv. " \
            "I found {} papers that you might be interested in ,Here are the list: {}"\
        .format(len(temp_paper_list),"\n".join(temp_paper_list))
    textApart=MIMEText(content)
    m=MIMEMultipart()
    m.attach(textApart)
    for i in temp_paper_list:
        add_apart(m,i+'.pdf')

    apart_file=date+'.csv'
    Apart=MIMEApplication(open('arxiv_daily/'+apart_file, 'rb').read())
    Apart.add_header('Content-Disposition', 'attachment', filename=apart_file)
    m.attach(Apart)

    m['Subject'] = 'Arxiv Paper Daily {}'.format(today)

    try:
        server=smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(from_address, password)
        server.sendmail(from_address, to_address, m.as_string())
        print('send Arxiv Paper Daily successfully!')
        server.quit()
    except smtplib.SMTPException as e:
        print('Error:', e)

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__=='__main__':

    mkdir('arxiv_daily/')
    mkdir('arxiv_paper/')
    key_word_list=['steganalysis','Steganalysis','attention','Attention']    # 关键词列表
    subject='cs.CV'                                                          # 相关主题
    items,date=get_paper_info_list(500)
    # target_paper_list=select_paper_by_title(key_word_list)
    target_paper_list=select_paper_mix(key_word_list,subject)
    temp_paper_list=download(target_paper_list)
    send_email(temp_paper_list,date)