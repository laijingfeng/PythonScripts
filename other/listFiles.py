#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-07 18:02:45

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

    files = []
    file_list = os.listdir(get_exe_path('./'))
    for file_name in file_list:
        if file_name.endswith('.py') or file_name.endswith('.pyc') or file_name.endswith('.log'):
            continue
        files.append(file_name)

    with open('listFiles.log', 'w') as f:
        for w in files:
            f.write(w + '\n')
