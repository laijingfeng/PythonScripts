# -*- coding: UTF-8 -*-

# 一个目录下，特定文件名重命名

import os, os.path, sys

def usage():
    print '---------usage---------'
    print 'python rename_files.py oldStr newStr [path]'
    print 'Example: python rename_files.py lai xiaolai D:\\tt'
    print '=========usage========='

if __name__ == '__main__':

    if(len(sys.argv) < 2):
        usage()
        exit()
    
    oldStr = sys.argv[1]
    newStr = sys.argv[2]
    if len(sys.argv) >= 4:
        tarPath = sys.argv[3]
    else:
        tarPath = os.getcwd()
            
# parent: parent dir
# dirnames: folders in this dir
# filenames: filenames in this dir

    for parent, dirnames, filenames in os.walk(tarPath):
        for filename in filenames:
            if filename.find(oldStr) != -1:
                newname = filename.replace(oldStr, newStr)
                os.rename(os.path.join(parent, filename), os.path.join(parent, newname))

    print 'Finish.'
