# !/usr/bin/python
# encoding=utf-8
# version: 2018-10-15 11:03:17
"""
Excel比较\n
列举两个Excel文件的差异，在日记文件里展示
"""

import sys
import os
import json
import codecs
import traceback
import subprocess
import xlrd
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))
from logger import Logger

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
        # 日志工具放前面，这个要尽量成功构建
        self.logger = Logger(Logger.LEVEL_INFO, self.get_exe_path(self.log_path))
        self.logger.reset()

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
            self.logger.error('Exception:')
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
            # 异常日志输出一份到控制台，方便调试及时看到
            print 'Exception:'
            print e
            print traceback.format_exc()

    def work(self):
        """
        实际工作逻辑
        """
        file_path1 = self.get_exe_path('./' + self.argv['file1'] + '.xlsx')
        file_path2 = self.get_exe_path('./' + self.argv['file2'] + '.xlsx')

        self.logger.info('compare excel: [{}] vs [{}].'.format(os.path.basename(file_path1), os.path.basename(file_path2)))
        
        if os.path.exists(file_path1) is False:
            self.logger.warn('can not find: {}'.format(file_path1))
            return
        
        if os.path.exists(file_path2) is False:
            self.logger.warn('can not find: {}'.format(file_path2))
            return

        work_book1 = xlrd.open_workbook(file_path1)
        work_book2 = xlrd.open_workbook(file_path2)
        
        sheet_cnt1 = len(work_book1.sheets())
        sheet_cnt2 = len(work_book2.sheets())

        if sheet_cnt1 != sheet_cnt2:
            self.logger.warn('sheet count not equal. [{}] vs [{}].'.format(sheet_cnt1, sheet_cnt2))
        sheet_cnt = sheet_cnt1
        if sheet_cnt2 < sheet_cnt:
            sheet_cnt = sheet_cnt2
        
        for idx in range(sheet_cnt):
            sheet1 = work_book1.sheets()[idx]
            sheet2 = work_book2.sheets()[idx]

            self.logger.info('')
            self.logger.info('compare sheet {}: [{}] vs [{}].'.format(idx, sheet1.name, sheet2.name))

            sheet_nrows1 = sheet1.nrows
            sheet_nrows2 = sheet2.nrows
            sheet_nrows = sheet_nrows1
            if sheet_nrows1 != sheet_nrows2:
                self.logger.warn('row count not equal. [{}] vs [{}].'.format(sheet_nrows1, sheet_nrows2))
            if sheet_nrows2 < sheet_nrows:
                sheet_nrows = sheet_nrows2

            for row_num in range(sheet_nrows):
                row_value1 = sheet1.row_values(row_num)
                row_value2 = sheet2.row_values(row_num)

                col_cnt1 = len(row_value1)
                col_cnt2 = len(row_value2)
                if col_cnt1 != col_cnt2:
                    self.logger.warn('column count not equal in row {}.'.format(row_num))
                col_cnt = col_cnt1
                if col_cnt2 < col_cnt:
                    col_cnt = col_cnt2

                for col_num in range(col_cnt):
                    # 转成字符串
                    val1 = str(row_value1[col_num])
                    val2 = str(row_value2[col_num])
                    if val1 != val2:
                        self.logger.warn('diff in {}{}: [{}] vs [{}].'.format(chr(col_num + ord('A')), row_num + 1, val1, val2))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
