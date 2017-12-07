#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-07 18:02:45

import sys
import os
import filecmp
import shutil

enter_cwd_dir = ''
python_file_dir = ''


def parse_arg(argv):
    if len(argv) != 3:
        return False, None
    return True, argv


def get_exe_path(simple_path):
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)


def usage():
    print 'this is usage()'
    print 'dirCmp.py oldDir newDir'

if __name__ == '__main__':
    success, args = parse_arg(sys.argv)
    if not success:
        usage()
        exit(-1)
    enter_cwd_dir = os.getcwd()
    python_file_dir = os.path.dirname(sys.argv[0])

    files = []
    x = filecmp.dircmp(args[1], args[2])
    if len(x.right_only) > 0:
        for w in x.right_only:
            files.append(w)
    if len(x.diff_files) > 0:
        for w in x.diff_files:
            files.append(w)

    file_list = os.listdir(get_exe_path(args[2]))
    for file_name in file_list:
        if files.count(file_name) == 1:
            shutil.copy(os.path.join(get_exe_path(args[2]), file_name), get_exe_path(file_name))

    with open('dirCmp.log', 'w') as f:
        for w in files:
            f.write(str(w) + '\n')
        f.write('===end')
