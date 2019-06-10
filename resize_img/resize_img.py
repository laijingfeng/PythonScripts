# !/usr/bin/python
# encoding=utf-8
# version: 2019-06-10
"""
图片缩放
"""

import sys
import os
from PIL import Image

enter_cwd_dir = ''
python_file_dir = ''

def get_exe_path(self, simple_path):
    """
    相对路径转绝对路径
    """
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)

def process_image(filepath, filename):
    new_dir = get_exe_path('./new/')
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

    # nw = 82
    # nh = 82
    
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
    reload(sys)
    sys.setdefaultencoding('utf-8')
    enter_cwd_dir = os.getcwd()
    python_file_dir = os.path.dirname(sys.argv[0])
    
    path = get_exe_path('./old/')
    list = os.listdir(path)
    for line in list:
        file_path = os.path.join(path, line)
        if os.path.isdir(file_path):
            continue
        if line.endswith('.png'):
            process_image(file_path, line)