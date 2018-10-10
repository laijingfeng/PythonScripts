# !/usr/bin/python
# encoding=utf-8
# version: 2018-10-10 10:17:46
"""
列举Bundle信息，名称和大小
"""

import sys
import os
import json
import codecs
import traceback
import subprocess

class ExeRsp(object):
    """
    执行命令返回值
    """
    def __init__(self):
        self.returncode = 0  # 返回值
        self.stderr = ''  # 错误

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
        self.config = {}  # 配置

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
        if os.path.exists(self.get_exe_path('./config.json')):
            with codecs.open(self.get_exe_path('./config.json'), 'r', 'utf-8') as file_handle:
                self.config = json.load(file_handle)

    @staticmethod
    def execute_shell_command(args, wait=True):
        """
        执行外部命令\n
        args 参数列表\n
        wait 是否等候
        """
        ret = ExeRsp()
        p = subprocess.Popen(args, stderr=subprocess.PIPE)
        if wait is True:
            ret.returncode = p.wait()
            ret.stderr = p.stderr.read()
            return ret
        else:
            ret.returncode = 0
            return ret

    def to_unicode(self, data):
        """
        数据转unicode
        """
        data = str(data).strip().decode('utf-8')
        return data
    
    def gbk_to_utf8(self, data):
        """
        gbk转utf8\n
        部分Windows软件使用gbk
        """
        data = str(data).strip().decode('gbk').encode('utf-8')
        return data
    
    def utf8_to_gbk(self, data):
        """
        utf8转gbk\n
        部分Windows软件使用gbk
        """
        data = str(data).strip().decode('utf-8').encode('gbk')
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
        try:
            self.__init_data__()
            self.work()
        except Exception as e:
            print 'Exception:'
            print e
            print traceback.format_exc()

    def work(self):
        """
        实际工作逻辑
        """
        find_files = []

        path = self.get_exe_path('./' + self.argv['path'] + '/')
        for parent, dirnames, filenames in os.walk(path): # path是相对路径
            for filename in filenames: # 包含了子文件夹的
                if filename.find('.') != -1:
                    continue
                file_path = os.path.join(parent, filename)
                bundle_name = file_path.replace(path, '')
                bundle_name = bundle_name.replace('\\', '/')
                find_files.append(FindFile(file_path, bundle_name))
        
        if len(find_files) > 1:
            find_files = sorted(find_files,  key=lambda FindFile:FindFile.bundle_name, reverse=False)
        
        with codecs.open('BundleInfo.txt', 'w', 'utf-8') as file_handler:
            for find_file in find_files:
                # print find_file.to_str()
                file_handler.write(find_file.to_str() + '\n')

class FindFile(object):
    def __init__(self, file_path, bundle_name):
        self.bundle_name = bundle_name
        self.bundle_size = os.path.getsize(file_path)
    def to_str(self):
        return '{}\t{}'.format(self.bundle_name, self.bundle_size)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
