# coding: utf-8
# version: 2018-01-01 22:03:54

import os
import sys
import shutil
import math
from PIL import Image, ImageDraw


def save_img(im, diff, d):
    draw = ImageDraw.Draw(im)
    step = 5
    for x in diff:
        draw.ellipse((x[0] - step, x[1] - step, x[0] + step, x[1] + step), fill=(255, 0, 0))
        draw.ellipse((x[0] - step, x[1] - step + d, x[0] + step, x[1] + step + d), fill=(0, 0, 255))
    del draw
    im.save('1_d.png')


def pull_screen():
    flag = os.system('adb shell screencap -p /sdcard/1.png')
    if flag == 1:
        print('adb is error')
        sys.exit()
    os.system('adb pull /sdcard/1.png .')


def main():
    pull_screen()

    # daily task
    # l1, t1 = 213, 166
    # l2, t2 = 213, 1027
    # w, h = 824, 824

    # pk
    l1, t1 = int(199 * 0.5), int(97 * 0.5)
    l2, t2 = int(199 * 0.5), int(997 * 0.5)
    w, h = int(824 * 0.5), int(824 * 0.5)

    im = Image.open('./1.png')
    im = im.resize((int(im.size[0] * 0.5), int(im.size[1] * 0.5)), Image.ANTIALIAS)

    im_pixel = im.load()
    diff = []
    cut_border = 5
    for x in range(0 + cut_border, w - cut_border, 10):
        for y in range(0 + cut_border, h - cut_border, 10):
            pix1 = im_pixel[l1 + x, t1 + y]
            pix2 = im_pixel[l2 + x, t2 + y]
            dist = abs(pix1[0] - pix2[0]) + abs(pix1[1] - pix2[1]) + abs(pix1[2] - pix2[2])
            if dist > 60:
                diff.append((l1 + x, t1 + y))
    save_img(im, diff, t2 - t1)


if __name__ == '__main__':
    main()
