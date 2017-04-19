#!/usr/bin/python
# encoding=utf-8
#version: 2017-04-19-00

# 说明：代码格式化
# 根据花括号填充tab(tab用4个空格)，删除多余的空格类字符
# 可以设置删除空行和压缩左括号
# 默认设定的是处理当前目录的cs文件

import sys, os
sys.path.append('..')
from logger import Logger

logger = Logger(Logger.LEVEL_INFO, 'code_composing')

def findFiles(path = '.'):
    list = os.listdir(path)
    for line in list:
        file_path = path + '\\' + line
        if os.path.isdir(file_path):
            continue
        if line.find('.cs') != -1:
            doFile(file_path)
            
def doFile(file_path):

    compress_left_bracket = False #是否压缩左括号，单独的左括号归到上一行
    #完善中...
    #可能退到注释行去了
    #回退到空行tab数不对

    delete_empty_line = False #是否删除空行

    if os.path.exists(file_path) == False:
        return
    
    ndata = []
    brackets_cnt = 0
    with open(file_path, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.strip()
            
            if len(d) <= 0:
                if delete_empty_line == False:
                    ndata.append('')
                continue

            t_c = d.count('{') - d.count('}')
            
            #多余的右括号要先减
            if t_c < 0 :
                brackets_cnt = brackets_cnt + t_c
                if brackets_cnt < 0:
                    brackets_cnt = 0
                t_c = 0

            if compress_left_bracket == True and len(d) == 1 and d[0] == '{' and len(ndata) > 0:
                ndata[len(ndata)-1] += '{'
            else:
                ndata.append((' ' * brackets_cnt * 4) + d)
            
            brackets_cnt = brackets_cnt + t_c
            if brackets_cnt < 0:
                brackets_cnt = 0
            
    with open(file_path, 'w') as f:
        for d in ndata:
            f.write(d + '\n')

def ParseArg(argv):
    if len(argv) == 2:
        return True, [argv[1]]
    elif len(argv) == 1:
        return True, ['']
    return False, None

def Usage():
    logger.info('------usage------')
    logger.info('`code_composing.py` for cs files in current folder')
    logger.info('`code_composing.py xx.xx` for file xx.xx')
    
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    find_file = args[0]
    if find_file == '':
        logger.info('work current folder')
        findFiles()
    else:
        logger.info('work file ' + find_file)
        doFile(find_file)
