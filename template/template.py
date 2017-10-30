#!/usr/bin/python
# encoding=utf-8
# version: 2017-10-30 11:31:05

import sys
import os

enter_cwd_dir = ''
python_file_dir = ''


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

    print 'start'
    print sys.argv[0], os.getcwd()
    os.chdir('D:/ADSafe')
    print sys.argv[0], os.getcwd()
    with open(get_exe_path('test.txt'), 'r') as f:
        read_data = f.readlines()
        for line in read_data:
            print line
