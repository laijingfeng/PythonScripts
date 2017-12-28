#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-20 16:43:36

import time
import sys
import ctypes
import win32con
import ctypes.wintypes
import win32gui
import autopy
import math
import threading
import pyHook
import pythoncom

start_pos = (0, 0)
end_pos = (0, 0)


# cmd win on the top
def topmost_me():
    hwnd = win32gui.GetForegroundWindow()
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, right - left, bottom - top, 0)


def on_keyboard_event(event):
    global start_pos
    global end_pos

    if event.Key == "A":
        start_pos = autopy.mouse.get_pos()
    elif event.Key == "S":
        end_pos = autopy.mouse.get_pos()
        one_step()
    elif event.Key == "Q":
        sys.exit()

    return True


def run():
    topmost_me()

    hm = pyHook.HookManager()
    hm.KeyDown = on_keyboard_event
    hm.HookKeyboard()
    pythoncom.PumpMessages()


def one_step():
    global start_pos
    global end_pos

    x = math.fabs(start_pos[0] - end_pos[0])
    y = math.fabs(start_pos[1] - end_pos[1])
    z = math.sqrt(x * x + y * y) / 415.0
    # autopy.mouse.move(322, 602)
    autopy.mouse.toggle(True)
    time.sleep(z)
    autopy.mouse.toggle(False)

    start_pos = end_pos


if __name__ == "__main__":
    run()
