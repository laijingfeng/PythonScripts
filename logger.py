#!/usr/bin/python
# encoding=utf-8
# version: 2017-08-24 17:50:15

import sys
import os
import ctypes
import shutil
from datetime import datetime


class Logger(object):
    LEVEL_ERROR = 3
    LEVEL_WARN = 2
    LEVEL_INFO = 1

    COLOR_BLACK = 0  # black.
    COLOR_DARKBLUE = 1  # dark blue.
    COLOR_DARKGREEN = 2  # dark green.
    COLOR_DARKSKYBLUE = 3  # dark skyblue.
    COLOR_DARKRED = 4  # dark red.
    COLOR_DARKPINK = 5  # dark pink.
    COLOR_DARKYELLOW = 6  # dark yellow.
    COLOR_DARKWHITE = 7  # dark white.
    COLOR_DARKGRAY = 8  # dark gray.
    COLOR_BLUE = 9  # blue.
    COLOR_GREEN = 10  # green.
    COLOR_SKYBLUE = 11  # skyblue.
    COLOR_RED = 12  # red.
    COLOR_PINK = 13  # pink.
    COLOR_YELLOW = 14  # yellow.
    COLOR_WHITE = 15  # white.

    foregroundColor = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    backgroundColor = [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0]

    def __init__(self, level=LEVEL_INFO, file_path='logger'):
        self.__level__ = level  # 最低打印等级
        self.__out_file__ = 1
        # 文件名可以设置，方便多个模块的日志区分
        self.__file_path__ = file_path

    @staticmethod
    def __set_cmd_color__(color):
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ret = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)
        return ret

    def __set_cmd_default_color__(self):
        self.__set_cmd_color__(self.foregroundColor[self.COLOR_WHITE] | self.backgroundColor[self.COLOR_BLACK])
    
    def __log__(self, level, content, fore_color=COLOR_WHITE, back_color=COLOR_BLACK):
        
        self.__set_cmd_color__(self.foregroundColor[fore_color] | self.backgroundColor[back_color])
        print '{}|{}|{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, content)
        self.__set_cmd_default_color__()
        
        if self.__out_file__ == 1:
            with open('{}.log'.format(self.__file_path__), 'a') as f:
                f.write('{}|{}|{}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, content))

    def set_config(self, level=LEVEL_INFO, file_path='logger'):
        self.__level__ = level
        self.__out_file__ = 1
        self.__file_path__ = file_path

    def reset(self):
        if os.path.exists(self.__file_path__ + '.log'):
            shutil.copy(self.__file_path__ + '.log', self.__file_path__ + '-prev.log')
            os.remove(self.__file_path__ + '.log')
        self.__log__('SYS', 'reset log')
        # 增加一句系统LOG，避免LOG为空，监听文件没了，同时也好看有响应

    def info(self, content, fore_color=COLOR_WHITE, back_color=COLOR_BLACK):
        if self.__level__ <= self.LEVEL_INFO:
            self.__log__('INFO', content, fore_color, back_color)

    def warn(self, content, fore_color=COLOR_YELLOW, back_color=COLOR_BLACK):
        if self.__level__ <= self.LEVEL_WARN:
            self.__log__('WARN', content, fore_color, back_color)

    def error(self, content, fore_color=COLOR_RED, back_color=COLOR_BLACK):
        if self.__level__ <= self.LEVEL_ERROR:
            self.__log__('ERROR', content, fore_color, back_color)
