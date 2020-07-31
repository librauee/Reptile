import requests
import re
import os
import time
import random
from tqdm import tqdm
import multiprocessing
import warnings
from lxml import etree
from glob import glob
from pypinyin import lazy_pinyin

warnings.filterwarnings("ignore")
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}


def get_m3u8_urls(vedio_name_py):
    """
    获取各分集的m3u8的url链接
    """
    vedio_url = 'http://www.diezhan.me/dalu/{}/'.format(vedio_name_py)
    r = requests.get(url=vedio_url, headers=headers)
    tree = etree.HTML(r.text)
    pieces = len(tree.xpath('//ul[@class="stui-content__playlist  sort-list column8 clearfix"]/li'))

    m3u8_urls = []
    for i in range(pieces):
        piece_url = 'http://www.diezhan.me/dalu/{}/play-0-{}.html'.format(vedio_name_py, i)
        r = requests.get(url=piece_url, headers=headers)
        m3u8_url = re.findall('now="(.*?index.m3u8)', r.text)[0]
        m3u8_url = m3u8_url[:-10] + '1000k/hls/' + m3u8_url[-10:]
        # print(m3u8_url)
        m3u8_urls.append(m3u8_url)

    return m3u8_urls

def run(vedio_name, process_number, ts_url_list, segs):
    """
    ts文件下载
    """
    for i in tqdm(range(segs)):
        r = requests.get(url = ts_url_list[process_number * segs + i],headers = headers, verify=False)
        with open('{}/{}'.format(vedio_name, ts_url_list[process_number * segs + i][-21:]), 'wb') as f:
            f.write(r.content)

def download(vedio_name, ts_url_list, segs):
    """
    多进程下载
    """
    record = []
    multiprocessing.freeze_support()
    for process_number in range(PROCESS_NUM):
        process = multiprocessing.Process(target=run, args=(vedio_name, process_number, ts_url_list, segs ))
        record.append(process)
        process.start()
    for _ in record:
        _.join()

def merge(piece):
    """
    合并ts文件
    """
    os.chdir(vedio_name)
    with open('temp.txt', 'w') as f:
        for ts_file in glob('*.ts'):
            f.write('file ' + ts_file + '\n')

    # shell_str = 'copy /b {} b.mp4'.format('+'.join(ts_list[300:600]))
    shell_str = 'ffmpeg -f concat -i temp.txt -c copy 第{}集.mp4'.format(piece + 1)
    os.system(shell_str)
    print("*****************视频'{}第{}集'合并成功*****************".format(vedio_name, piece+1))


def delete():
    """
    删除ts文件
    """
    shell_str = 'del *.ts *.txt'
    os.system(shell_str)
    print("*****************已删除所有ts文件以及临时文件！*****************")
    os.chdir("..")


def main(vedio_name):
    """
    主函数
    """
    vedio_name_py = "".join(lazy_pinyin(vedio_name))
    m3u8_urls = get_m3u8_urls(vedio_name_py)
    piece = 0
    for url in m3u8_urls:
        # 如果已存在，不进行下载
        if os.path.exists('{}/第{}集.mp4'.format(vedio_name, piece + 1)):
            piece += 1
            continue
        r = requests.get(url, headers=headers)
        m3u8_info = r.text.split("\n")
        ts_list = [i for i in m3u8_info if '.ts' in i]
        ts_url_list = [url[:-10] + i for i in ts_list]
        vedio_ts_number = len(ts_list)
        # print(len(ts_list))
        print("开始下载第{}集……".format(piece + 1))
        segs = vedio_ts_number // PROCESS_NUM
        download(vedio_name, ts_url_list, segs)
        merge(piece)
        time.sleep(1)
        delete()
        piece += 1

if __name__ == '__main__':

    vedio_name = input("请输入您要下载的电视剧：")
    if not os.path.exists(vedio_name):
        os.mkdir(vedio_name)
    PROCESS_NUM = 5
    main(vedio_name)











