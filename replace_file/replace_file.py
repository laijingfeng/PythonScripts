#!/usr/bin/python
# encoding=utf-8
# version: 2018-03-03 18:24:48
"""
替换文件\n
路径和文件名不支持中文
"""

import sys
import os
import json
import codecs

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
        self.config = {}  # 替换字典
        self.is_recursion = True  # 是否递归
        self.with_file_name = False  # 是否处理文件名
        self.with_file_content = True  # 是否处理文件内容
        self.replace_root = './files/'  # 要替换的根目录

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
        #         print len(pars), [pars[1]]
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
    def work_dir(self, path, deep):
        """
        处理一个目录
        """
        if deep > 0 and self.is_recursion is False:
            return
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isdir(file_path):
                self.work_dir(file_path, deep + 1)
            else:
                self.work_file(path, file_name)
    def work_file(self, file_dir, file_name):
        """
        处理一个文件
        """
        file_path = os.path.join(file_dir, file_name)
        if self.with_file_content:
            new_content = self.do_replace(codecs.open(file_path, 'rb', 'utf-8').read())
            codecs.open(file_path, 'wb', 'utf-8').write(new_content)
        if self.with_file_name:
            file_name_new = self.do_replace(file_name)
            if file_name != file_name_new:
                os.rename(file_path, os.path.join(file_dir, file_name_new))
    def do_replace(self, content):
        """
        替换
        """
        for key in self.config.keys():
            if content.count(key) > 0:
                content = content.replace(key, self.config[key])
        return content
    def work(self):
        """
        do real work
        """
        with codecs.open(self.get_exe_path('./config.json'), 'r', 'utf-8') as file_handle:
            self.config = json.load(file_handle)
        self.work_dir(self.get_exe_path(self.replace_root), 0)

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
