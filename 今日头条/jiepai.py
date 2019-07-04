# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 17:07:29 2019

@author: Administrator
"""

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re
import threading


def get_page(offset):
    headers = {
        'cookie': 'tt_webid=6667396596445660679; csrftoken=3a212e0c06e7821650315a4fecf47ac9; tt_webid=6667396596445660679; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16b846003e03d7-0dd00a2eb5ea11-353166-1fa400-16b846003e1566; CNZZDATA1259612802=2077267981-1561291030-https%253A%252F%252Fwww.baidu.com%252F%7C1561361230; __tasessionId=4vm71cznd1561363013083; sso_uid_tt=47d6f9788277e4e071f3825a3c36a294; toutiao_sso_user=e02fd616c83dff880adda691cd201aaa; login_flag=6859a0b8ffdb01687b00fe96bbeeba6e; sessionid=21f852358a845d783bdbe1236c9b385b; uid_tt=d40499ec45187c2d411cb7bf656330730d8c15a783bb6284da0f73104cd300a2; sid_tt=21f852358a845d783bdbe1236c9b385b; sid_guard="21f852358a845d783bdbe1236c9b385b|1561363028|15552000|Sat\054 21-Dec-2019 07:57:08 GMT"; s_v_web_id=6f40e192e0bdeb62ff50fca2bcdf2944',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    try:
        r = requests.get(url, headers=headers)
        if 200  == r.status_code:
            return r.json()
    except:
        return None


def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('title') is None:
                continue
            title = re.sub('[\t\\\|]', '', item.get('title'))
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list.*?pgc-image", "large/pgc-image", image.get('url'))
                yield {
                    'image': origin_image,
                    'title': title
                }


def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    r = requests.get(item.get('image'))
    file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(r.content).hexdigest(),
                file_suffix='jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(r.content)
        print("Downloaded image path is {}".format(file_path))
    else:
        print("Already Downloaded")




def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        try:           
            save_image(item)            
        except:
            print("下载图片失败！")


if __name__ == '__main__':
      
    #pool = Pool()     # 进程池
    groups = ([x * 20 for x in range(10)])
    '''
    pool.map(main, groups)
    pool.close()
    pool.join()
    '''
    tasks = []           # 线程池
    
    for group in groups:
        task = threading.Thread(target=main, args=(group,))
        tasks.append(task)
        task.start()
        
    # 等待所有线程完成
    for _ in tasks:
        _.join()         
    print("完成图片爬取并存储到本地！")
    