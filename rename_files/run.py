#! /usr/bin/env python
#coding=utf-8
#version: 2017-05-18-00

import os, os.path, sys

def Replace(text):
    global replaceDic
    for key in replaceDic:
        if text.count(key) > 0:
            text = text.replace(key, replaceDic[key])
    return text

def Usage():
    print 'this is Usage()'

replaceDic = {}

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    with open('replace.txt', 'r') as f:
        read_data = f.readlines()
        for line in read_data:
            line = line.strip()
            if(len(line) > 0):
                pars = line.split('-', 1)
                if len(pars) == 2:
                    replaceDic[pars[0]] = pars[1]

    for parent, dirnames, filenames in os.walk('./files/'):
        for filename in filenames:
            newname = Replace(filename)
            if filename != newname:
                os.rename(os.path.join(parent, filename), os.path.join(parent, newname))
                
