#!/usr/bin/python
# encoding=utf-8
# version: 2018-01-03 20:31:37

import time
import sys
import win32gui
import win32con
import os
import autopy
import math
import pyHook
import pythoncom
import json

enter_cwd_dir = ''
python_file_dir = ''
start_pos = (0, 0)
end_pos = (0, 0)
press_factor = 390
player_height = 10


def get_exe_path(simple_path):
    global enter_cwd_dir
    global python_file_dir
    return os.path.join(enter_cwd_dir, python_file_dir, simple_path)


def topmost_me():
    hwnd = win32gui.GetForegroundWindow()
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, right - left, bottom - top, 0)


def on_keyboard_event(event):
    if event.Key == "Q":
        sys.exit()
    return True


def on_mouse_event(event):
    global start_pos
    global end_pos

    if event.MessageName == 'mouse right down':
        start_pos = autopy.mouse.get_pos()
    elif event.MessageName == 'mouse right up':
        end_pos = autopy.mouse.get_pos()
        one_step()
    return True


def run():
    topmost_me()
    hm = pyHook.HookManager()
    hm.KeyDown = on_keyboard_event
    hm.HookKeyboard()
    hm.MouseAll = on_mouse_event
    hm.HookMouse()
    pythoncom.PumpMessages()


def one_step():
    global start_pos
    global end_pos
    global press_factor
    global player_height

    x = math.fabs(start_pos[0] - end_pos[0])
    y = math.fabs(start_pos[1] + player_height - end_pos[1])
    z = math.sqrt(x * x + y * y) / press_factor
    autopy.mouse.toggle(True)
    time.sleep(z)
    autopy.mouse.toggle(False)


if __name__ == "__main__":
    enter_cwd_dir = os.getcwd()
    python_file_dir = os.path.dirname(sys.argv[0])

    with open(get_exe_path('./config.json'), 'r') as f:
        config = json.load(f)
        press_factor = config['press_factor']
        player_height = config['player_height']
    run()


