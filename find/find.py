#!/usr/bin/python
# encoding=utf-8

import sys, os, re
from logger import Logger

logger = Logger(Logger.LOG_LEVEL_INFO, 'find')
find_path = '.'#'c:\\Users\\1\\AppData\\Local\\YNote\\Data\\xxx'

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
        with open('find_text.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                return True, [lines[0].strip()]
        #file_name = argv[0]
        #file_name = os.path.split(file_name)[1]
        #file_name = file_name.split('.')[0]
        #if file_name.find('_') != -1:
            #return True, [file_name.split('_')[1]]
    return False, None

def Usage():
    print '------usage------'
    print 'find.py text_want_to_find'
    print 'find.py with find_text.txt'
    #print 'find_xxx.py'

def MatchLine(line, words_want_to_find):
    cnt = 0
    idx = -1
    for w in words_want_to_find:
	idx = idx + 1
	if idx == 0 or idx == len(words_want_to_find) - 1:
	    continue
	m = re.search(w, line, re.IGNORECASE)
	if bool(m) == True or line.find(w) != -1:
	    cnt = cnt + 1
    return cnt

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    success, args = ParseArg(sys.argv)
    if not success:
        exit(-1)

    logger.reset()

    text_want_to_find = unicode(args[0],'utf-8')
    words_want_to_find = text_want_to_find.split('_')
    w_idx = -1
    finds = ''
    for w in words_want_to_find:
        w_idx = w_idx + 1
        if w_idx == 0 or w_idx == len(words_want_to_find) - 1:
            continue
        if finds == '':
            finds = finds + w
        else:
            finds = finds + '.' + w
    logger.info('find:' + finds)

    find_files = []
    
    for parent, dirnames, filenames in os.walk(find_path):
        for filename in filenames:
            if filename.find('.md') != -1:
                file_path = parent + '\\' + filename
                
                find_file = FindFile(parent, filename)

                #cnt = MatchLine(filename, words_want_to_find)
                #if cnt > 0:
                #    find_file.add_find(0, filename, cnt)
                    
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
