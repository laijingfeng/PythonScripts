# !/usr/bin/python
# version: 2019-06-26-00
"""
模版
"""

import sys
import os
import codecs
from main_class import MainClass

class WorkClass(MainClass):
    """
    工作类
    """
    def __init__(self):
        """
        初始化
        """
        MainClass.__init__(self)

        # 根据需要重新指定配置文件的路径
        self.log_path = './work'  # 日志文件名
        self.log_to_screen = True

        self.config_path = './config.json'  # 配置路径
    
    def work(self):
        """
        实际工作逻辑\n
        覆盖父类
        """
        # TODO 检查参数

        self.logger.info('==WorkClass开始==')
        
        # TODO...
        for key in self.config.keys():
            print('self.config[{}] = {}'.format(key, self.config[key]))
        for key in self.argv.keys():
            print('self.argv[{}] = {}'.format(key, self.argv[key]))

        with codecs.open(self.get_exe_path(os.path.join(self.config['project_root'], './set.svnprops')), 'rb', 'utf-8') as file_handle:
            read_data = file_handle.read()
            read_data_bytes = read_data.encode('utf-8')
            for d in read_data_bytes:
                print(d)

        self.logger.info('==WorkClass完成==')

if __name__ == '__main__':
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
