# !/usr/bin/python
# encoding=utf-8
# version: 2018-12-03
"""
图片缩放
"""

import os
from PIL import Image

def process_image(filepath, filename):
    new_dir = './new/'
    if os.path.exists(new_dir) is False:
        os.makedirs(new_dir)
    
    image = Image.open(filepath)
    w, h = image.size

    # 缩放比例
    scale = 0.7
    # 4的倍数
    need_4_scale = True

    nw = int(w * scale)
    nh = int(h * scale)
    
    if need_4_scale is True:
        wmod = nw % 4
        if wmod != 0:
            nw = nw + 4 - wmod
        hmod = nh % 4
        if hmod != 0:
            nh = nh + 4 - hmod
    
    new_im = image.resize((nw, nh), Image.ANTIALIAS)     
    new_im.save(new_dir + filename)

if __name__ == '__main__':
    path = './old/'
    list = os.listdir(path)
    for line in list:
        file_path = os.path.join(path, line)
        if os.path.isdir(file_path):
            continue
        if line.endswith('.png'):
            process_image(file_path, line)