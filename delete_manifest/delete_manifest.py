# !/usr/bin/python
# encoding=utf-8
# version: 2017-12-31 17:52:35

import sys
import os
import json

enter_cwd_dir = ''
python_file_dir = ''
test_name = ''
test_age = ''

def parse_arg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv


def get_exe_path(simple_path):
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)


def usage():
    print 'this is usage()'

if __name__ == '__main__':
    success, args = parse_arg(sys.argv)
    if not success:
        usage()
        exit(-1)
    enter_cwd_dir = os.getcwd()
    python_file_dir = os.path.dirname(sys.argv[0])

    for parent, dirnames, filenames in os.walk('./'): # path是相对路径
        for filename in filenames: # 包含了子文件夹的
            file_path = os.path.join(parent, filename)
            if filename.find('.manifest') != -1:
                print file_path
                os.remove(file_path)