# !/usr/bin/python
# encoding=utf-8
# version: 2018-03-19 00:35:05
"""
收集依赖
"""

import sys
import os
import json
import codecs
import wx
import shutil
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
        
        dir_drop = FileDropTarget(self.m_textCtrl_dir)
        self.m_textCtrl_dir.SetDropTarget(dir_drop)

        save_drop = FileDropTarget(self.m_textCtrl_save)
        self.m_textCtrl_save.SetDropTarget(save_drop)

        json_drop = FileDropTarget(self.m_textCtrl_json)
        self.m_textCtrl_json.SetDropTarget(json_drop)

        self.has_error = False

        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
    
    def get_exe_path(self, simple_path):
        """
        相对路径转绝对路径
        """
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    
    def onClickReplace(self, event):
        self.m_textCtrl_tip.SetValue('提示：处理中...')
        if self.m_textCtrl_dir.GetValue() == '' \
            or self.m_textCtrl_json.GetValue() == '' \
            or self.m_textCtrl_save.GetValue() == '':
            self.m_textCtrl_tip.SetValue('提示：参数不完整')
            return False
        if self.m_checkBox_clean.GetValue():
            shutil.rmtree(self.m_textCtrl_save.GetValue())
            os.makedirs(self.m_textCtrl_save.GetValue())
        self.has_error = False
        self.work_one_config(self.m_textCtrl_json.GetValue())
        if self.has_error is False:
            self.m_textCtrl_tip.SetValue('提示：处理完成')

    def work_one_config(self, path):
        """
        处理一个配置文件
        """
        if os.path.exists(path) is False:
            return
        config = {}
        with codecs.open(self.get_exe_path(path), 'r', 'utf-8') as file_handle:
            config = json.load(file_handle)
        for key in config['dependencies']:
            self.work_one_dll(key)
    
    def work_one_dll(self, filename):
        """
        处理一个dll
        """
        path = self.find_dll_path(filename)
        if path == '':
            self.has_error = True
            self.m_textCtrl_tip.SetValue('提示：can not find {}'.format(filename))
            return
        
        dll_path = os.path.join(path, filename)
        dll_path_target = os.path.join(self.m_textCtrl_save.GetValue(), filename)
        if os.path.exists(dll_path_target):
            os.remove(dll_path_target)
        shutil.copy(dll_path, dll_path_target)

        config_path = dll_path.replace('.dll', '.json')
        self.work_one_config(config_path)
    
    def find_dll_path(self, find_filename):
        """
        查找dll路径
        """
        for parent, dirnames, filenames in os.walk(self.m_textCtrl_dir.GetValue()):
            for filename in filenames:
                if filename == find_filename:
                    return parent
        return ''

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
