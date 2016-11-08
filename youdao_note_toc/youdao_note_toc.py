#!/usr/bin/python
# encoding=utf-8

import sys, os
sys.path.append('..')
from logger import Logger

logger = Logger(Logger.LEVEL_INFO, 'note_toc')

def findFiles(path = '.'):
    list = os.listdir(path)
    for line in list:
        file_path = path + '\\' + line
        if os.path.isdir(file_path):
            continue
        if line.find('.md') != -1 and line != 'ok.md':
            doFile(file_path)
            
def doFile(file_path):
    logger.info('do:' + file_path)
    ndata = []
    finds = ['### ','## ','# ']
    finds2 = ['--------','----','']
    last_line = 'aaaaaeeee'
    with open(file_path, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.rstrip()

            fs_idx = -1
            for i in range(len(finds)):
                if d.find(finds[i]) == 0:
                    fs_idx = i
                    break

            if fs_idx != -1:
                real_title = d[len(finds[fs_idx]):]
                old_idx = real_title.find('[^')
                if old_idx != -1 and old_idx != 0:
                    real_title = real_title[:old_idx]
                    last_line = real_title[old_idx:]
                else:
                    last_line = 'aaaaaeeee'
                ndata.append(finds[fs_idx] + real_title + '[^' + real_title + ']')
                ndata.append('[^' + real_title + ']: ' + finds2[fs_idx] + real_title)
                continue
            if d.find(last_line) != 0:
                ndata.append(d)
            last_line = 'aaaaaeeee'
    with open('ok.md', 'w') as f:
        for d in ndata:
            f.write(d + '\n')

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    logger.reset()
    findFiles()
    
