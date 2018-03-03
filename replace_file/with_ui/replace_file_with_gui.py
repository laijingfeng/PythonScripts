#!/usr/bin/python
# encoding=utf-8
# version: 2018-03-03 19:53:43
"""
替换文件\n
路径和文件名不支持中文
"""

import sys
import os
import json
import codecs
import wx
import replace_file_ui

class MainFrame(replace_file_ui.MainFrameUI):
    def __init__(self,parent):
        replace_file_ui.MainFrameUI.__init__(self, parent)
        dropTarget = FileDropTarget(self.m_text_dir)
        self.m_text_dir.SetDropTarget(dropTarget)

        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
        self.config = {}  # 替换字典
    
    def get_exe_path(self, simple_path):
        """
        相对路径转绝对路径
        """
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    
    def onClickReplace(self, event):
        self.m_textCtrl_tip.SetValue('提示：处理中...')
        self.config.clear()
        rule_val = self.m_textCtrl_rule.GetValue()
        rules = rule_val.split('\n')
        for v in rules:
            vs = v.split(']-[')
            if len(vs) == 2:
                self.config[vs[0][1:len(vs[0])]] = vs[1][0:len(vs[1]) - 1]
        if self.work_dir(self.m_text_dir.GetValue(), 0):
            self.m_textCtrl_tip.SetValue('提示：处理完成')

    def work_dir(self, path, deep):
        """
        处理一个目录
        """
        if path == '':
            self.m_textCtrl_tip.SetValue('提示：请先设置目录')
            return False
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

class FileDropTarget(wx.FileDropTarget):  
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self, x, y, fileNames):
        self.window.SetValue(str(fileNames[0]))  

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
