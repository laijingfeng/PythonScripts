# !/usr/bin/python
# encoding=utf-8
# version: 2019-05-27
"""
图片转换成字符图
"""

import sys
import os
import codecs
from main_class import MainClass
from PIL import Image

class WorkClass(MainClass):
    def __init__(self):
        MainClass.__init__(self)

        # 根据需要重新指定配置文件的路径
        self.log_path = './work_ascii'  # 日志文件名
        self.log_to_screen = True

        self.config_path = './config_ascii.json'  # 配置路径
    
    def get_char(self, r, g , b, alpha=256):
        if alpha == 0:
            return ''
        length = len(self.argv['chars'])
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length
        return self.argv['chars'][int(gray / unit)]

    def work(self):
        """
        实际工作逻辑\n
        覆盖父类
        """
        self.argv['img_path'] = self.get_exe_path('./test.png')
        self.argv['img_width'] = 100
        self.argv['img_height'] = 100
        self.argv['out_path'] = self.get_exe_path('./ascii_out.txt')
        self.argv['chars'] = 'abcdefghijklmnopqrstuvwxy '

        img = Image.open(self.argv['img_path'])
        img = img.resize((self.argv['img_width'], self.argv['img_height']), Image.NEAREST)

        txt = ''
        for i in range(self.argv['img_height']):
            for j in range(self.argv['img_width']):
                txt += self.get_char(*img.getpixel((j, i)))
            txt += '\n'
        with codecs.open(self.argv['out_path'], 'w', 'utf-8') as file_handler:
            file_handler.write(txt)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
