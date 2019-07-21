# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 08:28:59 2019

@author: Lee
"""
import requests
import re
from fontTools.ttLib import TTFont




def get_new_ttf(url):
    """
    输入：网页链接
    输出：新字体以及网页源代码
    """
    r1=requests.get(url,headers=headers)
    ttf=re.findall(r",url\('(//.*\.ttf)'\)",r1.text)[0]
    r=requests.get('https:'+ttf)
    with open('new.ttf','wb') as f:
        f.write(r.content)
    font2=TTFont('new.ttf')
    # font2.saveXML('font_2.xml')
    return font2,r1.text
    
    
def compare(c1,c2):
    """
    输入：某俩个对象字体的坐标列表
    输出：bool类型，True则可视为是同一个字
    """
    if len(c1)!=len(c2):
        return False
    else:
        for i in range(len(c1)):
            if abs(c1[i][0]-c2[i][0])<50 and abs(c1[i][1]-c2[i][1])<50:
                pass
            else:
                return False
        return True

def decrypt_font(font1,font2,response):
    """
    输入：base字体，新字体以及网页源代码
    输出：字体解密后的网页源代码
    """
    word_list=['九','呢','着','地','得','的','五','六','低','右','一','二','远','更','了','好','三','多','小','长','是','坏','十','近','少','八','很','四','短','上','七','下','不','和','高','左','矮','大']
    uniname_list1=['uniEC1F', 'uniEC21', 'uniEC39', 'uniEC3B', 'uniEC55', 'uniEC67', 'uniEC71', 'uniEC81', 'uniEC82', 'uniEC8B', 'uniEC9D', 'uniECAE', 'uniECB7', 'uniECB8', 'uniECD3', 'uniECE4', 'uniECED', 'uniECFE', 'uniED00', 'uniED09', 'uniED18', 'uniED1A', 'uniED34', 'uniED36', 'uniED46', 'uniED50', 'uniED61', 'uniED6A', 'uniED7C', 'uniED96', 'uniED97', 'uniEDB2', 'uniEDC3', 'uniEDCC', 'uniEDCD', 'uniEDDD', 'uniEDE8', 'uniEDF9']
    uniname_list2=font2.getGlyphNames()[1:]
    base_dict=dict(zip(uniname_list1,word_list))
    
    # 保存每个字符的坐标信息，分别存入coordinate_list1和coordinate_list2
    coordinate_list1=[]     
    for uniname in uniname_list1:
        # 获取字体对象的横纵坐标信息
        coordinate=font1['glyf'][uniname].coordinates 
        coordinate_list1.append(list(coordinate))

    coordinate_list2=[]
    for i in uniname_list2:
        coordinate=font2['glyf'][i].coordinates
        coordinate_list2.append(list(coordinate))

    index2=-1
    new_dict={}
    for name2 in coordinate_list2:
        index2+=1
        index1=-1
        for name1 in coordinate_list1:           
            index1+=1
            if compare(name1,name2):
                new_dict[uniname_list2[index2]]=base_dict[uniname_list1[index1]]
                
    for uniname in uniname_list2:
        pattern='&#x'+uniname[3:].lower()+';'
        response=re.sub(pattern,new_dict[uniname],response)
    return response
            
            
            
            
            
if __name__ == '__main__':   
         
    font1=TTFont('base.ttf')
    # font.saveXML('font_1.xml')
    headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie": "fvlid=1563667948613fkOHKfG2zR; sessionip=114.213.210.86; sessionid=BDFE3D02-CE41-4D60-8D53-5277BD287ECF%7C%7C2019-07-21+08%3A12%3A27.462%7C%7Cwww.baidu.com; autoid=c3a5376fa8c6cf9ca92ff9ceb0176be2; sessionvid=CBD6AA01-530C-475E-AC39-EF6C90CE57DF; area=340111; ahpau=1; sessionuid=BDFE3D02-CE41-4D60-8D53-5277BD287ECF%7C%7C2019-07-21+08%3A12%3A27.462%7C%7Cwww.baidu.com; __ah_uuid_ng=c_BDFE3D02-CE41-4D60-8D53-5277BD287ECF; cookieCityId=110100; ahpvno=9; pvidchain=3311277,3454442,3311253,6826817,6826819; ref=www.baidu.com%7C0%7C0%7C0%7C2019-07-21+08%3A44%3A19.829%7C2019-07-21+08%3A12%3A27.462; ahrlid=1563669858351rrF6xJuLHZ-1563669896292",
            "Host": "club.autohome.com.cn"}
    url='https://club.autohome.com.cn/bbs/thread/e27f0f48dcb56de8/81875131-1.html'
    font2,response=get_new_ttf(url)
    after_decrypt_response=decrypt_font(font1,font2,response)
    print(after_decrypt_response)
          
          


    

