# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:09:07 2019

@author: Lee
"""

from hashlib import md5
a="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
print(md5(a.encode('utf-8')).hexdigest())