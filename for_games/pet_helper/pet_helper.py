#!/usr/bin/python
# encoding=utf-8
# version: 2017-12-21 11:33:08

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

L, T = 5, 27  # left-top position, 游戏在模拟器的白边开始算
EXIT = False  # had exit


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


# 获取hash
def get_hash(img):
    image = img.resize((15, 15), Image.ANTIALIAS).convert("L")
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join(map(lambda p: "1" if p > avg else "0", pixels))


# 计算距离
def hamming_dist(hash1, hash2):
    return sum(itertools.imap(operator.ne, hash1, hash2))


def touch():
    l, t = L + 22, T + 176
    r, b = l + 49, t + 50
    # ImageGrab.grab((l, t, r, b)).save('touch_t.png')
    hash_val1 = get_hash(ImageGrab.grab((l, t, r, b)))
    hash_val2 = get_hash(Image.open('touch.png'))
    dis = hamming_dist(hash_val1, hash_val2)
    if dis < 50:
        print 'touch', dis
        # return True
        autopy.mouse.move(l + 25, t + 25)
        autopy.mouse.click()
        time.sleep(1)
        return True
    return False


def gold(idx):
    l, t = L + 19, T + 261
    r, b = l + 53, t + 44
    # ImageGrab.grab((l, t, r, b)).save('gold_t.png')
    hash_val1 = get_hash(ImageGrab.grab((l, t, r, b)))
    hash_val2 = get_hash(Image.open('gold.png'))
    dis = hamming_dist(hash_val1, hash_val2)
    if dis < 50:
        print 'gold', dis
        # return True
        autopy.mouse.move(l + 25, t + 25)
        autopy.mouse.click()
        time.sleep(0.5)
        if idx < 5:
            autopy.mouse.move(L + 394, T + 725)  # help
            autopy.mouse.click()
            time.sleep(0.5)
            # may be help is full, should try rob to done task, so it will not close immediately
        autopy.mouse.move(L + 163, T + 725)  # rob
        autopy.mouse.click()
        time.sleep(0.5)
        autopy.mouse.move(L + 506, T + 234)  # close, if can not rob, should manual close
        autopy.mouse.click()
        return True
    return False


# return 0 for can not, 1 for can but not, for can and do
def hit():
    l, t = L + 21, T + 335
    r, b = l + 50, t + 50
    # ImageGrab.grab((l, t, r, b)).save('hit_t.png')
    hash_val1 = get_hash(ImageGrab.grab((l, t, r, b)))
    hash_val2 = get_hash(Image.open('hit.png'))
    dis = hamming_dist(hash_val1, hash_val2)
    if dis < 50:
        print 'hit', dis
        # return True
        autopy.mouse.move(l + 25, t + 25)
        autopy.mouse.click()
        time.sleep(0.5)

        l1, t1 = L + 342, T + 343
        r1, b1 = l1 + 53, t1 + 43
        hash_val11 = get_hash(ImageGrab.grab((l1, t1, r1, b1)))
        hash_val21 = get_hash(Image.open('can_hit.png'))
        dis1 = hamming_dist(hash_val11, hash_val21)
        # ImageGrab.grab((l1, t1, r1, b1)).save('can_hit_t.png')
        print 'can_hit', dis1
        if dis1 < 50:  # judge if can hit
            autopy.mouse.move(L + 280, T + 650)  # click pet
            for i in xrange(13):
                autopy.mouse.click()
                time.sleep(1.0)
            autopy.mouse.move(L + 280, T + 504)  # click gold
            autopy.mouse.click()
            time.sleep(0.2)
            return 2
        return 1
    return 0


def run():
    topmost_me()
    hot_key = HotKey()
    hot_key.start()

    done_touch = False
    done_gold = False
    done_hit = False
    select_idx = 0
    idx = 0
    while True:
        if EXIT:
            sys.exit()
        if done_touch is False:
            if touch() is True:
                done_touch = True
            time.sleep(0.5)
            continue

        if done_gold is False:
            if gold(idx) is True:
                done_gold = True
            time.sleep(0.5)
            continue

        if done_hit is False:
            hit_val = hit()
            if hit_val == 1 or hit_val == 2:
                if hit_val == 1:
                    select_idx = select_idx + 1
                    if select_idx > 5:
                        select_idx = 0
                done_hit = True
            time.sleep(0.5)
            continue

        print 'done_friend', idx
        idx = idx + 1
        done_touch = False
        done_gold = False
        done_hit = False

        autopy.mouse.move(L + 504, T + 909)  # other friend
        autopy.mouse.click()
        time.sleep(0.5)

        autopy.mouse.move(L + 494 - select_idx * 88, T + 901)  # select friend
        autopy.mouse.click()
        time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
