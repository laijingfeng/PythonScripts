#!/usr/bin/python
# encoding=utf-8
# version: 2018-03-09 13:54:42
"""
收集依赖
"""

import sys
import os
import json
import codecs
import wx
import collect_dependency_ui

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self, x, y, fileNames):
        self.window.SetValue(str(fileNames[0]))

class MainFrame(collect_dependency_ui.MainFrameUI):
    def __init__(self,parent):
        collect_dependency_ui.MainFrameUI.__init__(self, parent)
        
        dir_drop = FileDropTarget(self.m_text_dir)
        self.m_text_dir.SetDropTarget(dir_drop)

        save_drop = FileDropTarget(self.m_textCtrl_save)
        self.m_textCtrl_save.SetDropTarget(save_drop)

        json_drop = FileDropTarget(self.m_textCtrl_json)
        self.m_textCtrl_json.SetDropTarget(json_drop)

        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
    
    def get_exe_path(self, simple_path):
        """
        相对路径转绝对路径
        """
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    
    def onClickReplace(self, event):
        self.m_textCtrl_tip.SetValue('提示：处理中...')
        if self.m_text_dir.GetValue() == '' \
            or self.m_textCtrl_json.GetValue() == '' \
            or self.m_textCtrl_save.GetValue() == '':
            self.m_textCtrl_tip.SetValue('提示：参数不完整')
            return False
        
        self.m_textCtrl_tip.SetValue('提示：处理完成')

    def work_dir(self, path, deep):
        """
        处理一个目录
        """
        if deep > 0 and self.m_checkBox_recursion.GetValue() is False:
            return True
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isdir(file_path):
                self.work_dir(file_path, deep + 1)
            else:
                self.work_file(path, file_name)
        return True
    def work_file(self, file_dir, file_name):
        """
        处理一个文件
        """
        file_path = os.path.join(file_dir, file_name)
        if self.m_checkBox_with_content.GetValue():
            new_content = self.do_replace(codecs.open(file_path, 'rb', 'utf-8').read())
            codecs.open(file_path, 'wb', 'utf-8').write(new_content)
        if self.m_checkBox_with_name.GetValue():
            file_name_new = self.do_replace(file_name)
            if file_name != file_name_new:
                os.rename(file_path, os.path.join(file_dir, file_name_new))
    def do_replace(self, content):
        """
        替换
        """
        for key in self.config.keys():
            if content.count(key) > 0:
                content = content.replace(key, self.config[key])
        return content

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
