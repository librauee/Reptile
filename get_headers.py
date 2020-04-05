# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:17:19 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

# 请求头格式脚本

import re

headers="""

"""

pattern='^(.*?): (.*)$'

# \1表示重复正则第一个圆括号内匹配到的内容
for line in headers.splitlines():
    print(re.sub(pattern,'\'\\1\':\'\\2\',',line))
    
    
