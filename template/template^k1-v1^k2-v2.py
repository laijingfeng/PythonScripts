# !/usr/bin/python
# encoding=utf-8
# version: 2018-06-22 13:21:53
"""
工具模板
"""

import sys
import os
import json
import codecs
sys.path.append('..')
from logger import Logger

class MainClass(object):
    """
    主类
    """
    def __init__(self):
        """
        初始化
        """
        self.enter_cwd_dir = ''  # 执行路径
        self.python_file_dir = ''  # python文件路径
        self.argv = {}  # 参数，文件名参考：template^k1-v1^k2-v2.py
        self.config = ''  # 配置

        self.log_path = './work'  # 日志文件名
        self.logger = ''  # 日志工具

    def parse_argv(self):
        """
        解析参数\n
        返回是否成功
        """
        if len(sys.argv) < 1:
            return False
        # 解析文件名参数
        if len(sys.argv) == 1:
            file_name = sys.argv[0]
            file_name = os.path.split(file_name)[1]  # 去掉目录
            file_name = file_name.split('.')[0]  # 去掉后缀
            if file_name.count('^') > 0:
                pars = file_name.split('^', 1)[1]  # 去掉文件名
                self.parse_give_argv(pars)
        else:
            self.parse_give_argv(sys.argv[1])
        return True
    
    def parse_give_argv(self, argvs):
        """
        解析指定参数\n
        独立出来，也可以手动执行
        """
        pars = argvs.split('^')  # 分离参数
        for par in pars:
            if par.find('-') != -1:
                par_key = par.split('-', 1)[0]
                par_val = par.split('-', 1)[1]
                self.argv[par_key] = par_val
    
    def usage(self):
        """
        使用说明，参数不对的时候会提示
        """
        print 'this is usage()'
    
    def __init_data__(self):
        """
        初始化数据，解析参数之后
        """
        with codecs.open(self.get_exe_path('./config.json'), 'r', 'utf-8') as file_handle:
            self.config = json.load(file_handle)
        self.logger = Logger(Logger.LEVEL_INFO, self.get_exe_path(self.log_path))
        self.logger.reset()

    def to_unicode(self, data):
        """
        数据转unicode
        """
        data = str(data).strip().decode('utf-8')
        return data
    
    def get_exe_path(self, simple_path):
        """
        相对路径转绝对路径
        """
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    
    def run(self):
        """
        类入口
        """
        success = self.parse_argv()
        if not success:
            self.usage()
            exit(-1)
        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
        self.__init_data__()
        self.work()
    
    def work(self):
        """
        do real work
        """
        for key in self.config.keys():
            print 'self.config[{}] = {}'.format(key, self.config[key])
        for key in self.argv.keys():
            print 'self.argv[{}] = {}'.format(key, self.argv[key])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
