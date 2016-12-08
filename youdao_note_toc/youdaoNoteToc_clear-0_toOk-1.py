#!/usr/bin/python
# encoding=utf-8

import sys, os, shutil, datetime
sys.path.append('..')
from logger import Logger

new_to_ok = True
clear_toc = False
ok_file_name = 'toc_ok.md'
logger = Logger(Logger.LEVEL_INFO, 'note_toc')

def findFiles(path = '.'):
    list = os.listdir(path)
    for line in list:
        file_path = path + '\\' + line
        if os.path.isdir(file_path):
            continue
        if line.find('.md') != -1 and line != ok_file_name and line.find('.bak') == -1:
            doFile(file_path)
            
def doFile(file_path):
    logger.info('do:' + file_path)
    ndata = []
    finds = ['#### ','### ','## ','# ']
    finds2 = ['------------','--------','----','']
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
                    
                if clear_toc == True:
                    ndata.append(finds[fs_idx] + real_title)
                else:
                    ndata.append(finds[fs_idx] + real_title + '[^' + real_title + ']')
                    ndata.append('[^' + real_title + ']: ' + finds2[fs_idx] + real_title)
                continue
            if d.find(last_line) != 0:
                ndata.append(d)
            last_line = 'aaaaaeeee'

    new_file = ok_file_name
    if new_to_ok == False:
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        destf= '.'.join((file_path,ts,'bak'))
        shutil.copy(file_path, destf)
        new_file = file_path
    
    with open(new_file, 'w') as f:
        for d in ndata:
            f.write(d + '\n')
            
def ParseArg(argv):
    global new_to_ok
    global clear_toc
    new_to_ok = True
    clear_toc = False
        
    if len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]
        file_name = file_name.split('_',1)[1]
        
        pars = file_name.split('_')
        for p in pars:
            ps = p.split('-')
            if len(ps) == 2:
                if ps[0] == 'clear':
                    if ps[1] == '0':
                        clear_toc = False
                    elif ps[1] == '1':
                        clear_toc = True
                elif ps[0] == 'toOK':
                    if ps[1] == '0':
                        new_to_ok = False
                    elif ps[1] == '1':
                        new_to_ok = True

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    logger.reset()
    ParseArg(sys.argv)
    logger.info('clear_toc=' + str(clear_toc) + ' new_to_ok=' + str(new_to_ok))
    findFiles()
