# !/usr/bin/python
# encoding=utf-8
# version: 2018-04-15 00:20:50
"""
代码模板
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
        self.enter_cwd_dir = ''  # 执行路径
        self.python_file_dir = ''  # python文件路径
        self.argv = {}  # 参数，模板只解析了文件名参数，参考：template^k1-v1^k2-v2.py
        self.config = ''  # 配置

    def parse_argv(self):
        """
        解析参数\n
        返回是否成和参数列表
        """
        if len(sys.argv) < 1:
            return False, None
        # 解析文件名参数
        if len(sys.argv) == 1:
            file_name = sys.argv[0]
            file_name = os.path.split(file_name)[1]  # 去掉目录
            file_name = file_name.split('.')[0]  # 去掉后缀
            pars = file_name.split('^', 1)[1]  # 去掉文件名
            pars = pars.split('^')  # 分离参数
            if len(pars) > 1:
                for par in pars:
                    if par.find('-') != -1:
                        par_key = par.split('-', 1)[0]
                        par_val = par.split('-', 1)[1]
                        self.argv[par_key] = par_val
        return True, sys.argv
    
    def usage(self):
        """
        使用说明，参数不对的时候会提示
        """
        print 'this is usage()'
    
    def __init_data__(self):
        """
        初始化数据
        """
        pass

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
        success, args = self.parse_argv()
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
            self.config = json.load(file_handle)
        for key in self.config.keys():
            print 'self.config[{}] = {}'.format(key, self.config[key])
        for key in self.argv.keys():
            print 'self.argv[{}] = {}'.format(key, self.argv[key])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
