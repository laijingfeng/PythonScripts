#!/usr/bin/python
#-*-coding:utf-8-*-
# version: 2018-01-22 14:48:44
"""code template"""

import sys
import os
import json
import hashlib

class MainClass(object):
    """main class"""
    def __init__(self):
        """init the class"""
        self.enter_cwd_dir = ''
        self.python_file_dir = ''
    def parse_arg(self):
        """parse input args"""
        if len(sys.argv) < 1:
            return False, None
        return True, sys.argv
    def get_exe_path(self, simple_path):
        """get the direct path"""
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    def usage(self):
        """just the usage description of this code"""
        print 'this is usage()'
    def run(self):
        """enter the class"""
        success, args = self.parse_arg()
        if not success:
            self.usage()
            exit(-1)
        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
        self.work()
    def cal_md5(self, file_path):
        """cal md5"""
        md5_val = ''
        with open(file_path, 'rb') as f:
            md5_val = hashlib.md5(f.read()).hexdigest()
        return md5_val
    def work(self):
        """do real work"""
        with open(self.get_exe_path('./config.json'), 'r') as read_file:
            config = json.load(read_file)
        test_name = config['test_name']
        test_age = config['test_age']
        print test_name, test_age
        print self.cal_md5('./config.json')

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
