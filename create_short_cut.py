#!/usr/bin/python
# encoding=utf-8
# version: 2017-10-23 19:46:22

import sys
import os
import winshell

enter_cwd_path = ''


def parse_arg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv


def get_exe_path(simple_path):
    global enter_cwd_path
    return os.path.join(enter_cwd_path, os.path.dirname(sys.argv[0]), simple_path)


def usage():
    print 'this is usage()'


def create_shortcut(target_path, shortcut_path):
    winshell.CreateShortcut(
        Path = shortcut_path,
        Target = target_path,
        Icon = (target_path, 0),
        Description = 'my shortcut')

if __name__ == '__main__':
    success, args = parse_arg(sys.argv)
    if not success:
        usage()
        exit(-1)
    enter_cwd_path = os.getcwd()
    create_shortcut(get_exe_path('./toc.py'), get_exe_path('./toc.py.lnk'))

    
