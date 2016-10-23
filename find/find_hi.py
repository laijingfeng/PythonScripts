#!/usr/bin/python
# encoding=utf-8

import sys, os
from logger import Logger

logger = Logger(Logger.LOG_LEVEL_INFO)

class FindFile(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.finds = []
        
    def add_find(self, line_idx, line_txt):
        self.finds.append('Line.{}:{}'.format(line_idx, line_txt))
        
    def output(self):
        if len(self.finds) <= 0:
            return
        logger.info('----------------------------------------')
        logger.info(self.file_path)
        for find in self.finds:
            logger.info(find)

def ParseArg(argv):
    if len(argv) == 2:
        return True, [argv[1]]
    elif len(argv) == 1:
        file_name = os.path.split(argv[0])[1]
        file_name = file_name.split('.')[0]
        if file_name.find('_') != -1:
            return True, [file_name.split('_')[1]]
    return False, None

def Usage():
    print '------usage------'
    print 'find.py text_want_to_find'
    print 'find_xxx.py'

if __name__ == '__main__':
    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)

    logger.reset()
    text_want_to_find = args[0]
    logger.info('find:' + text_want_to_find)

    for parent, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.find('.md') != -1:
                file_path = parent + '\\' + filename

                find_file = FindFile(file_path)
                
                line_idx = 0
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.find(text_want_to_find) != -1:
                            find_file.add_find(line_idx, line)
                        line_idx = line_idx + 1

                find_file.output()
                    
    
