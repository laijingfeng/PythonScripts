#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-30 10:46:46

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
config = 390
boy_height = 10


# cmd win on the top
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
    global config
    global boy_height

    x = math.fabs(start_pos[0] - end_pos[0])
    y = math.fabs(start_pos[1] + boy_height - end_pos[1])
    z = math.sqrt(x * x + y * y) / config
    autopy.mouse.toggle(True)
    time.sleep(z)
    autopy.mouse.toggle(False)


def img_val(img, l, t, r, b):
    ret = 0
    for x in range(l, r):
        for y in range(t, b):
            pix = img.getpixel((x, y))
            for z in range(3):
                ret += pix[z]
    return ret


if __name__ == "__main__":
    with open('config.txt', 'r') as f:
        read_data = f.readlines()
        config = float(read_data[0])
        boy_height = float(read_data[1])
    run()


