# !/usr/bin/python
# encoding=utf-8
# version: 2018-04-14 23:58:51
"""
拷贝SVN
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
        self.config = ''

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
    def to_unicode(self, data):
        """
        数据转unicode
        """
        data = str(data).strip().decode('utf-8')
        return data
    def work(self):
        """
        do real work
        """
        with codecs.open(self.get_exe_path('./config.json'), 'r', 'utf-8') as file_handle:
            self.config = json.load(file_handle)
        dir_from = self.get_exe_path(self.config['dir_from'])
        dir_to = self.get_exe_path(self.config['dir_to'])
        if self.config['work'] == 'return':  # 重现
            self.delete(dir_to)
            self.copy_dir(dir_from, dir_to)
        elif self.config['work'] == 'backup':  # 备份
            self.copy_dir(dir_from, dir_to)
        else:
            print 'no cmd'

    def delete(self, root_dir):
        """
        清除
        """
        check_path = [
            './common/',
            "./client/game/",
            "./client/src/",
        ]
        for p in check_path:
            work_path = os.path.join(root_dir, p)
            if os.path.exists(work_path):
                shutil.rmtree(work_path)
    def copy_dir(self, dir_from, dir_to):
        dir_from = self.to_unicode(dir_from)
        if os.path.exists(dir_from) is False:
            return
        if os.path.isdir(dir_from) is False:
            return
        name_from = os.path.split(dir_from)[1]
        for p in self.config['except']:
            if p == name_from:
                return
        tmp = os.path.split(dir_from)[0]
        name_from2 = os.path.split(tmp)[1] + '/' + name_from
        for p in self.config['except2']:
            if p == name_from2:
                return

        if not os.path.exists(dir_to):
            os.makedirs(dir_to)

        list = os.listdir(dir_from)
        for f in list:
            dir_from2 = os.path.join(dir_from, f)
            dir_to2 = os.path.join(dir_to, f)
            if os.path.isdir(dir_from2):
                self.copy_dir(dir_from2, dir_to2)
            else:
                need = True
                for p in self.config['except_file_tag']:
                    if self.to_unicode(dir_from2).find(p) != -1:
                        need = False
                        break
                if need is True:
                    shutil.copy(dir_from2, dir_to2)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
