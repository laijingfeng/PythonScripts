#!/usr/bin/python
# encoding=utf-8
# version: 2017-08-24 16:56:55

import sys


def parse_arg(argv):
    if len(argv) < 1:
        return False, None
    return True, argv


def usage():
    print 'this is usage()'

if __name__ == '__main__':
    success, args = parse_arg(sys.argv)
    if not success:
        usage()
        exit(-1)
    print 'start'
