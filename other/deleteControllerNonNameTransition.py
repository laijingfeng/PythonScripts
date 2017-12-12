#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-12 12:21:30

import sys
import os

enter_cwd_dir = ''
python_file_dir = ''


def parse_arg(argv):
    if len(argv) != 1:
        return False, None
    return True, argv


def get_exe_path(simple_path):
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)


def usage():
    print 'this is usage()'


def handle_file(file_path):
    file_content = []
    with open(file_path, 'r') as f:
        file_content = f.readlines()

    have_bad = False
    for i in range(0, len(file_content))[::-1]:
        if (have_bad is True) and file_content[i].strip().startswith('--- !u!'):
            file_content[i] = 'ToDelete' + file_content[i].lstrip()
            have_bad = False
        if file_content[i].strip() == 'm_Name:':
            file_content[i] = file_content[i].rstrip() + ' ToDelete\n'
            have_bad = True

    with open(file_path, 'wb') as f:
        to_jump = False
        for w in file_content:
            if w.strip().startswith('--- !u!'):
                to_jump = False
            elif w.strip().startswith('ToDelete--- !u!'):
                to_jump = True
            if to_jump is True:
                continue
            if w.strip() == 'm_Name: XXX':
                w = '  m_Name: '
            f.write(w.rstrip() + chr(0x0A))

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
        if file_name.endswith('.controller'):
            handle_file(get_exe_path(os.path.join('./', file_name)))
