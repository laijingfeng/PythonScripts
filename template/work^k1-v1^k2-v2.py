# !/usr/bin/python
# encoding=utf-8
# version: 2018-11-11 23:54:34
"""
模版
"""

import sys
import os
from main_class import MainClass

class WorkClass(MainClass):
    def __init__(self):
        MainClass.__init__(self)

        # 根据需要重新指定配置文件的路径
        self.log_path = './work'  # 日志文件名
        self.config_path = './config.json'  # 配置路径
    
    def work(self):
        """
        实际工作逻辑\n
        覆盖父类
        """
        self.logger.info('==WorkClass开始==')
        
        # TODO...
        for key in self.config.keys():
            print 'self.config[{}] = {}'.format(key, self.config[key])
        for key in self.argv.keys():
            print 'self.argv[{}] = {}'.format(key, self.argv[key])

        self.logger.info('==WorkClass完成==')

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
