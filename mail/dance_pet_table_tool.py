#!/usr/bin/python
#-*-coding:utf-8-*-
# version: 2018-01-24 15:14:54
"""dance pet tool"""

import sys
import os
import codecs
import json
from collections import OrderedDict
import ftplib
import xlrd

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
    def upload_to_ftp(self, upload_type):
        """upload files to ftp"""
        host = '106.15.181.140'
        username = 'test1'
        password = 'eYYFEJjt'
        f = ftplib.FTP()
        f.set_pasv(False)
        f.set_debuglevel(0)
        f.connect(host, 21, 25)
        f.login(username, password)
        path_is_right = False
        try:
            f.cwd('gawumengchong3d/test/res/' + upload_type)
            path_is_right = True
        except Exception as error:
            print error.message
            path_is_right = False
        if path_is_right is False:
            print '[error]: ftp error {}'.format(upload_type)
            f.quit()
            return False
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and (filename.startswith('~') is False):
                if (upload_type == 'tables' and filename.endswith('.json')) or (upload_type == 'sound' and filename.endswith('.mp3')):
                    fp = open(filename, 'rb')
                    f.storbinary('STOR ' + filename, fp, 1024 * 1024)
                    print '[info]: upload file : {}'.format(filename)
                    fp.close()
        f.quit()
        return True
    def clean(self):
        """clean files"""
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and (filename.startswith('~') is False):
                if filename.endswith('.json'):
                    os.remove(filename)
    def excel_to_json(self):
        """excel to json return whether success"""
        ret = False
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and filename.endswith('.xlsx') and (filename.startswith('~') is False):
                convert_list = []
                work_book = xlrd.open_workbook(filename)
                sheet = work_book.sheet_by_index(0)
                title = sheet.row_values(0)
                data_type = sheet.row_values(1)
                for row_num in range(3, sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    single = OrderedDict()
                    for col_num in range(0, len(row_value)):
                        if data_type[col_num] == 'string':
                            single[title[col_num]] = str(row_value[col_num]).replace('.0', '')
                        elif data_type[col_num] == 'int':
                            single[title[col_num]] = int(row_value[col_num])
                        else:
                            single[title[col_num]] = row_value[col_num]
                    convert_list.append(single)
                j = json.dumps(convert_list)
                with codecs.open(filename.replace('.xlsx', '.json'), 'w', 'utf-8') as file_handler:
                    file_handler.write(j)
                ret = True
        if ret is False:
            print "[info]: no table need handle"
        else:
            print "[info]: table ok"
        return ret
    def any_key_exit(self):
        """any key to exit"""
        os.system('pause')
    def work(self):
        """do real work"""
        if self.excel_to_json() is True:
            self.upload_to_ftp('tables')
            self.clean()
        self.upload_to_ftp('sound')
        print "===Tool Work Finish==="
        self.any_key_exit()

if __name__ == '__main__':
    GET_MAIL = MainClass()
    GET_MAIL.run()
