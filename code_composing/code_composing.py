#!/usr/bin/python
# encoding=utf-8

import sys, os

def findFiles(path = '.'):
    list = os.listdir(path)
    for line in list:
        file_path = path + '\\' + line
        if os.path.isdir(file_path):
            continue
        if line.find('.cs') != -1:
            doFile(file_path)
            
def doFile(file_path):
    ndata = []
    brackets_cnt = 0
    with open(file_path, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.strip()
            
            if len(d) <= 0:
                ndata.append('')
                continue

            t_c = d.count('{') - d.count('}')
            
            #多余的右括号要先减
            if t_c < 0 :
                brackets_cnt = brackets_cnt + t_c
                if brackets_cnt < 0:
                    brackets_cnt = 0
                t_c = 0

            ndata.append((' ' * brackets_cnt * 4) + d)
            
            brackets_cnt = brackets_cnt + t_c
            if brackets_cnt < 0:
                brackets_cnt = 0
            
    with open(file_path, 'w') as f:
        for d in ndata:
            f.write(d + '\n')

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    findFiles()
