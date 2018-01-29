#!/usr/bin/python
# encoding=utf-8
# version: 2018-01-29 15:17:39
"""
代码模板
"""

import sys
import os
import json

class MainClass(object):
    """
    主类
    """
    def __init__(self):
        """
        初始化
        """
        self.enter_cwd_dir = ''
        self.python_file_dir = ''

    def __init_data__(self):
        """
        初始化数据
        """
        pass

    def parse_arg(self):
        """
        解析参数\n
        返回是否成和参数列表
        """
        if len(sys.argv) < 1:
            return False, None
        # 解析文件名参数
        # if len(sys.argv) == 1:
        #     file_name = sys.argv[0]
        #     file_name = os.path.split(file_name)[1]
        #     file_name = file_name.split('.')[0]
        #     pars = file_name.split('^')
        #     if len(pars) > 1:
        #         print len(pars), pars[1]
        return True, sys.argv
    def get_exe_path(self, simple_path):
        """
        相对路径转绝对路径
        """
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    def usage(self):
        """
        使用说明，参数不对的时候会提示
        """
        print 'this is usage()'
    def run(self):
        """
        类入口
        """
        success, args = self.parse_arg()
        if not success:
            self.usage()
            exit(-1)
        if args is None:
            pass  # 这句只是为了去掉提示变量未使用
        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
        self.__init_data__()
        self.work()
    def work(self):
        """
        do real work
        """
        with open(self.get_exe_path('./config.json'), 'r') as read_file:
            config = json.load(read_file)
        test_name = config['test_name']
        test_age = config['test_age']
        print test_name, test_age

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
