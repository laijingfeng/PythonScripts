# !/usr/bin/python
# version: 2019-06-26-00
"""
模版
"""

import sys
import os
import wx # gui
from main_frame_ui import MainFrameUI # gui
from main_class import MainClass

class WorkClass(MainClass, MainFrameUI):
    """
    工作类
    """
    def __init__(self):
        """
        初始化
        """
        MainClass.__init__(self)
        MainFrameUI.__init__(self, None) # gui

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

        self.logger.info('==WorkClass完成==')
    
    def onClickMy(self, event):
        """
        重写MainFrameUI的点击事件
        """
        self.logger.info('onClickMy')

if __name__ == '__main__':
    app = wx.App(False) # gui
    WORK_CLASS = WorkClass()
    WORK_CLASS.run()
    WORK_CLASS.Show(True) # gui
    app.MainLoop() # gui
