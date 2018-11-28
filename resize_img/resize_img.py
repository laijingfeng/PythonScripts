# !/usr/bin/python
# encoding=utf-8
# version: 2018-11-28
"""
图片缩放
"""

import os
from PIL import Image

def process_image(filename):
    new_dir = './new/'
    if os.path.exists(new_dir) is False:
        os.makedirs(new_dir)
    
    image = Image.open(filename)
    w, h = image.size
    scale = 0.7
    new_im = image.resize((int(w * scale), int(h * scale)), Image.ANTIALIAS)     
    new_im.save(new_dir + filename)

if __name__ == '__main__':
    path = './old/'
    list = os.listdir(path)
    for line in list:
        file_path = os.path.join(path, line)
        if os.path.isdir(file_path):
            continue
        if line.endswith('.png'):
            process_image(line)