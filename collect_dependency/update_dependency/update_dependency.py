# !/usr/bin/python
# encoding=utf-8
# version: 2018-03-22 17:55:05
"""
更新依赖文件的版本
"""

import sys
import os
import json
import codecs
import shutil

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
        self.dll_lib_dir = ''

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
    def work(self):
        """
        do real work
        """
        with codecs.open(self.get_exe_path('./config.json'), 'r', 'utf-8') as file_handle:
            config = json.load(file_handle)
            self.dll_lib_dir = self.get_exe_path(config['dll_lib_dir'])
        
        root_dir = self.get_exe_path('./')
        file_list = os.listdir(root_dir)
        for line in file_list:
            file_path = os.path.join(root_dir, line)
            if os.path.isdir(file_path):
                continue
            if line.endswith('.dll'):
                self.work_one_dll(line)
    def find_dll_path(self, find_filename):
        """
        查找dll路径
        """
        for parent, dirnames, filenames in os.walk(self.dll_lib_dir):
            for filename in filenames:
                if filename == find_filename:
                    return parent
        return ''
    def work_one_dll(self, filename):
        """
        处理一个dll
        """
        path = self.find_dll_path(filename)
        if path == '':
            return
        dll_path = os.path.join(path, filename)
        dll_path_target = os.path.join(self.get_exe_path('./'), filename)
        if os.path.exists(dll_path_target):
            os.remove(dll_path_target)
        shutil.copy(dll_path, dll_path_target)

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
