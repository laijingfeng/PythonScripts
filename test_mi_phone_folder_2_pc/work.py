# !/usr/bin/python
# encoding=utf-8
# version: 2018-11-13 15:45:00
"""
模版
"""

import sys
import os
import time
from ftplib import FTP
from main_class import MainClass

class WorkClass(MainClass):
    def __init__(self):
        MainClass.__init__(self)

        # 根据需要重新指定配置文件的路径
        self.log_path = './work'  # 日志文件名
        self.log_to_screen = False

        self.config_path = './config.json'  # 配置路径
    
    def work(self):
        """
        实际工作逻辑\n
        覆盖父类
        """
        # TODO 检查参数

        self.logger.info('==WorkClass开始==')
        
        self.src_dir = 'ftp://172.16.0.249:2121/'
        self.tar_dir = self.get_exe_path('./data/')

        ftp = FTP()
        ftp.connect('172.16.0.249', '2121')
        ftp.login()
        
        # ftp.set_debuglevel(2)

        self.walk_ftp(ftp, '/Android/data')
        # while True:
        #     cmd_code = raw_input('--->input cmd:')
        #     if cmd_code == 'q' or cmd_code == 'Q':
        #         break
        #     elif cmd_code == 'i' or cmd_code == 'I':
        #         print '==PWD==\n' + ftp.pwd()
        #     elif cmd_code == 'l' or cmd_code == 'L':
        #         print '==List=='
        #         file_list = ftp.nlst()
        #         for line in file_list:
        #             print line
        #     else:
        #         try:
        #             ftp.cwd(cmd_code)
        #         except Exception as error:
        #             print error.message
        # ftp.set_debuglevel(0)
        ftp.quit()
        self.logger.info('==WorkClass完成==')
    
    def walk_ftp(self, ftp, p_dir):
        tar_file_dir_sub = os.path.join(self.tar_dir, '.' + p_dir)
        try:
            ftp.cwd(p_dir)
        except Exception as error:
            return

        file_list = ftp.nlst()
        for line in file_list:
            tar_file_path = os.path.join(tar_file_dir_sub, line)
            if not os.path.exists(tar_file_path):
                os.makedirs(tar_file_path)
        
        time.sleep(0.1)

        for line in file_list:
            if p_dir != '/':
                self.walk_ftp(ftp, p_dir + '/' + line)
            else:
                self.walk_ftp(ftp, p_dir + line)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
