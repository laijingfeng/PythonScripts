#!/usr/bin/python
# encoding=utf-8
# version: 2018-01-07 23:18:56

import sys
import os
import json
import time
import zmq

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

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv()
        print message
        dic = {"type":"server_rsp", "from":"lai", "time":time.time()}
        socket.send(json.dumps(dic))