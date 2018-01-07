#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-31 17:52:35

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
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        data = raw_input("input your data")
        if data == 'q':
            sys.exit()
        dic = {"type":"client_req", "msg":data}
        socket.send(json.dumps(dic))
        response = socket.recv()
        print response