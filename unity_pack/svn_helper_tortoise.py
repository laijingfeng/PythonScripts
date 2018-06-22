# !/usr/bin/python
# encoding=utf-8
# version: 2018-04-11 23:53:19

import os


class SvnHelperTortoise(object):
    """
    TortoiseSvn助手
    """
    def __init__(self):
        pass

    @classmethod
    def update(cls, path):
        """
        更新
        """
        os.system("TortoiseProc.exe /command:update /path:\"" + path + "\" /notempfile /closeonend:2")

    @classmethod
    def commit(cls, path):
        """
        提交
        """
        os.system("TortoiseProc.exe /command:commit /path:\"" + path + "\" /logmsg:\"" + '' + "\" /notempfile /closeonend:2")
