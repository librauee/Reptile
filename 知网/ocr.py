# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 17:13:56 2019

@author: Lee
"""

import tesserocr
from PIL import Image

image=Image.open('code.jpg')
image=image.convert('L')
threshold=127
table=[]
for i in range(256):
    if i<threshold:
        table.append(0)
    else:
        table.append(1)
        
image=image.point(table,'1')
print(tesserocr.image_to_text(image))