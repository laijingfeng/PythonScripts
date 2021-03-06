# !/usr/bin/python
# encoding=utf-8
# version: 2018-04-28 01:25:28

import sys
import os
import re
import json
import codecs
sys.path.append('..')
from logger import Logger

logger = Logger(Logger.LEVEL_INFO, 'do_find')
config = ''  # 配置

class FindFile(object):
    def __init__(self, file_dir, file_name):
        self.file_dir = file_dir
        self.file_name = file_name
        self.finds = []
        self.weight = 0
        
    def add_find(self, line_idx, line_txt, cnt = 1):
        self.weight += max(1, 1000 - line_idx * 10) * pow(2, cnt - 1)
        self.finds.append('Line.{}:{}'.format(line_idx, line_txt))

    def get_weight(self):
        return self.weight
        
    def output(self):
        if len(self.finds) <= 0:
            return
        logger.info('----------------------------------------')
        logger.info('path:' + self.file_dir)
        logger.info('name:' + self.file_name)
        for find in self.finds:
            logger.info(find.strip())

def ParseArg(argv):
    if len(argv) == 2:
        return True, [argv[1]]
    elif len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]
        if file_name.find('_') != -1:
            return True, [file_name.split('_', 1)[1]]
    return False, None

def Usage():
    logger.info('------usage------')
    logger.info('`find.py xx1_xx2` give par')
    logger.info('`find_xx1_xx2.py` read par from name')

def MatchLine(line, words_want_to_find):
    cnt = 0
    for w in words_want_to_find:
	m = re.search(w, line, re.IGNORECASE)
	if bool(m) == True or line.find(w) != -1:
	    cnt = cnt + 1
    return cnt

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    #if not success:
    #    Usage()
    #    exit(-1)
    args = ['Show in Explorer']

    logger.reset()
    with codecs.open('./config.json', 'r', 'utf-8') as file_handle:
        config = json.load(file_handle)
    
    text_want_to_find = args[0].decode('gb2312').encode('utf8')
    words_want_to_find = text_want_to_find.split('_')

    logger.info('find:' + text_want_to_find)
    find_files = []
    
    for parent, dirnames, filenames in os.walk(config['work_path']):
        for filename in filenames:
            if filename.find(config['file_flag']) != -1:
                file_path = os.path.join(parent, filename)
                find_file = FindFile(parent, filename)

                #标题
                cnt = MatchLine(filename, words_want_to_find)
                if cnt > 0:
                    find_file.add_find(0, filename, cnt)
                    
                #内容
                line_idx = 1
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        cnt = MatchLine(line, words_want_to_find)
                        if cnt > 0:
                            find_file.add_find(line_idx, line, cnt)
                        line_idx = line_idx + 1

                if find_file.get_weight() > 0:
                    find_files.append(find_file)

    if len(find_files) > 1:
        find_files = sorted(find_files,  key=lambda FindFile:FindFile.weight, reverse=True)
        
    for find_file in find_files:
        find_file.output()
