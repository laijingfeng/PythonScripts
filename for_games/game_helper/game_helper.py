#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-20 16:43:36

import itertools
import operator
import time
import sys
import threading
import ctypes
import win32con
import ctypes.wintypes
import win32gui
import autopy
import Image
import ImageGrab

L, T = 51, 210  # left-top position
EXIT = False  # had exit


# 菜单
class Menu:
    def __init__(self):
        self.stuff_pos = []
        self.recipes = [None] * 8
        self.init_stuff()
        self.init_recipe()

    # 初始化9种原料
    def init_stuff(self):
        for i in range(9):
            # 原料的左上角位置
            self.stuff_pos.append((L + 102 + (i % 3) * 42, T + 303 + (i / 3) * 42))

    # 初始化8种食谱
    def init_recipe(self):
        self.recipes[0] = (1, 2)
        self.recipes[1] = (0, 1, 2)
        self.recipes[2] = (5, 1, 2)
        self.recipes[3] = (3, 0, 1, 2)
        self.recipes[4] = (4, 1, 2)
        self.recipes[5] = (7, 1, 2)
        self.recipes[6] = (6, 1, 2)
        self.recipes[7] = (8, 1, 2)

    # 点击一种原料
    def click(self, i):
        autopy.mouse.move(self.stuff_pos[i][0] + 20, self.stuff_pos[i][1] + 20)
        autopy.mouse.click()

    # 制作一个菜
    def make(self, i):
        for x in self.recipes[i]:
            self.click(x)
        autopy.mouse.move(L + 315, T + 363)
        autopy.mouse.click()


class Custom:
    def __init__(self):
        self.menu = Menu()
        self.left = L + 47  # 第1个客人头顶冒泡的最左
        self.top = T + 53  # 第1个客人头顶冒泡的最高
        self.width = 53  # 冒泡的宽度
        self.height = 39  # 冒泡的高度
        self.step = 126  # 相邻两个冒泡最左的距离
        self.bottom = T + 243  # 底部，桌子的位置
        self.maps = [None] * 12  # 可能要的12种菜

        for i in xrange(12):
            try:
                self.maps[i] = self.get_hash(Image.open(str(i) + ".png"))
            except IOError:
                pass

    # 下单，返回菜谱的编号
    def order(self, i):
        l, t = self.left + i * self.step, self.top
        r, b = l + self.width, t + self.height
        hash2 = self.get_hash(ImageGrab.grab((l, t, r, b)))
        (mi, dist) = None, 50
        for i, hash1 in enumerate(self.maps):
            if hash1 is None:
                continue
            this_dist = self.hamming_dist(hash1, hash2)
            if this_dist < dist:
                mi = i
                dist = this_dist
        return mi

    # 要制作的食物
    def serve1(self, i, mi):
        self.menu.make(mi)
        time.sleep(0.5)
        autopy.mouse.move(L + 315, T + 363)
        autopy.mouse.toggle(True)
        time.sleep(0.2)
        autopy.mouse.smooth_move(self.left + self.step * i + 20, self.bottom)
        time.sleep(0.2)
        autopy.mouse.toggle(False)

    # 要现成的调料
    def serve2(self, i, mi):
        if mi == 10:
            autopy.mouse.move(L + 466, T + 410)
        elif mi == 9:
            autopy.mouse.move(L + 466, T + 360)
        elif mi == 8:
            autopy.mouse.move(L + 466, T + 320)
        else:
            autopy.mouse.move(L + 543, T + 320)
        autopy.mouse.toggle(True)
        time.sleep(0.2)
        autopy.mouse.smooth_move(self.left + self.step * i + 20, self.bottom)
        time.sleep(0.2)
        autopy.mouse.toggle(False)

    # 获取hash
    @staticmethod
    def get_hash(img):
        image = img.resize((18, 13), Image.ANTIALIAS).convert("L")
        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        return "".join(map(lambda p: "1" if p > avg else "0", pixels))

    # 计算距离
    @staticmethod
    def hamming_dist(hash1, hash2):
        return sum(itertools.imap(operator.ne, hash1, hash2))


# Win + F3 is the hot key to exit
class HotKey(threading.Thread):
    def run(self):
        global EXIT
        user32 = ctypes.windll.user32
        print "Register exit hotkey"
        if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F3):
            raise RuntimeError
        try:
            msg = ctypes.wintypes.MSG()
            print msg
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == 99:
                        EXIT = True
                        return
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, 1)


# cmd win on the top
def topmost_me():
    hwnd = win32gui.GetForegroundWindow()
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, right - left, bottom - top, 0)


# 判断点击下一关
def judge_next():
    l, t = L + 400, T + 138
    r, b = l + 88, t + 88
    hash_val = Custom.get_hash(ImageGrab.grab((l, t, r, b)))
    dis = Custom.hamming_dist(hash_val, Custom.get_hash(Image.open('next.png')))
    if dis < 50:
        autopy.mouse.move(l + 44, t + 44)
        autopy.mouse.click()
        return True
    return False


def run():
    topmost_me()
    hot_key = HotKey()
    hot_key.start()

    custom = Custom()
    while True:
        if judge_next() is False:
            for i in xrange(4):  # 遍历4个顾客
                if EXIT:
                    sys.exit()
                eat_first = True 
                while True:  # 后期可能1个顾客连着吃好几个 
                    if EXIT:
                        sys.exit()
                    if eat_first is False:
                        time.sleep(0.2)
                    m = custom.order(i)          
                    if m is not None:
                        eat_first = False
                        if m < 8:
                            custom.serve1(i, m)
                        else:
                            custom.serve2(i, m)
                        print '{} eat {}'.format(i, m)
                    else:
                        break
                        # print '{} no custom'.format(i)
        time.sleep(0.5)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        custom = Custom()
        hash2 = custom.get_hash(Image.open(sys.argv[1]))
        print "***", hash2
        for i, h in enumerate(custom.maps):
            if h is None:
                continue
            print "%2d: %s" % (i, h)
            print "==>", custom.hamming_dist(h, hash2)
