import requests
import re
from fontTools.ttLib import TTFont
from pymongo import MongoClient


def get_woff_id():
    """
    获取字体文件的id，同时也是path参数
    """
    url='https://lottery.8oe.com/history/txffc.html'
    r=requests.get(url,headers=headers)
    woff_id=re.findall("font='(.*?)',_length",r.text)[0]
    return woff_id

def get_woff_file(woff_id):
    """
    下载字体文件到本地
    """
    url='https://lottery.8oe.com/fonts/woff/id/{}'.format(woff_id)
    r=requests.get(url,headers=headers)
    with open('a.woff','wb') as f:
        f.write(r.content)

def trans(code,font_map):
    """
    字体编码转换
    """
    for i in font_map.keys():
        pattern='&#x'+i[2:]+';'
        code=re.sub(pattern,str(font_map[i]),code)
    return code

def get_data(woff_id,font_map):
    """
    数据获取，转换后存入数据库
    """
    url='https://lottery.8oe.com/index/get_histcodes1128.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://lottery.8oe.com',
        'Referer': 'https://lottery.8oe.com/history/txffc.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '54',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest'
        }

    data={
        'code': '32',
        #'date': '2020-06-05',
        'path': woff_id,
        'limit': '60',
    }
    r=requests.post(url,headers=headers,data=data)
    print(r.text)
    count=r.json()['count']
    infos=r.json()['data']
    for info in infos:
        info_time=info['time']
        issue=info['issue']
        code=info['code']
        print(code)
        trans_code=trans(code,font_map)
        print(trans_code)
        item={
            'info_time':info_time,
            'code':trans_code,
            'issue':issue
        }
        db['ffc'].insert_one(item)
    max_page=int(count/60)+1 if count%60!=0 else int(count/60)
    for page in range(2,max_page):
        data={
            'code': '32',
            # 'date': '2020-06-05',
            'path': woff_id,
            'limit': '60',
            'page': str(page)
        }
        r=requests.post(url, headers=headers, data=data)
        infos=r.json()['data']
        for info in infos:
            info_time=info['time']
            issue=info['issue']
            code=info['code']
            print(code)
            trans_code=trans(code, font_map)
            print(trans_code)
            item={
                'info_time': info_time,
                'code': trans_code,
                'issue': issue
            }
            db['ffc'].insert_one(item)


def get_new_name_list(font,name_list):
    """
    获取字体name属性
    """
    new_name_list=[]
    for name in name_list:
        glyf=font['glyf'][name]
        if hasattr(glyf, 'coordinates') and name.startswith('glyph'):
            new_name_list.append(name)
    return new_name_list


def get_font_map():
    """
    获取code和数字的映射表
    """
    font1=TTFont('base.woff')
    #font1.saveXML('font_base.xml')
    base_dict={'glyph00009': 7, 'glyph00013': 2, 'glyph00018': 1, 'glyph00023': 6, 'glyph00028': 9, 'glyph00030': 8,
                 'glyph00034': 4, 'glyph00039': 5, 'glyph00044': 3, 'glyph00048': 0}
    name_list1=font1.getGlyphNames()

    font2=TTFont('a.woff')
    #font2.saveXML('font_1.xml')
    name_list2=font2.getGlyphNames()

    new_name_list1=get_new_name_list(font1, name_list1)
    new_name_list2=get_new_name_list(font2, name_list2)
    print(new_name_list1)
    print(new_name_list2)
    # 获取name与数字的映射关系
    new_dict={}
    for name2 in new_name_list2:
        coord_list2=font2['glyf'][name2].coordinates
        for name1 in new_name_list1:
            coord_list1=font1['glyf'][name1].coordinates
            if coord_list1[:10]==coord_list2[:10]:
                new_dict[name2]=base_dict[name1]
    print(new_dict)
    font_map={}
    # 使用getBestCmap方法来获取name和code的映射关系
    for key, value in font2.getBestCmap().items():
        if value in new_dict.keys():
            font_map[hex(key)]=new_dict[value]
    print(font_map)
    return font_map

if __name__=='__main__':

    db=MongoClient().lottery
    woff_id=get_woff_id()
    get_woff_file(woff_id)
    font_map=get_font_map()
    get_data(woff_id,font_map)