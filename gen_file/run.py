#! /usr/bin/env python
#coding=utf-8
#version: 2017-04-13-00

import sys, os
import shutil

def DoClean(path):
    for f in os.listdir(path):
        sf = os.path.join(path, f)
        if os.path.isfile(sf):
            os.remove(sf)
        if os.path.isdir(sf):
            shutil.rmtree(sf)

def Replace(text):
    global replaceDic
    for key in replaceDic:
        if text.count(key) > 0:
            text = text.replace(key, replaceDic[key])
    return text

def CopyFiles(sDir, tDir):
    for f in os.listdir(sDir):
        sf = os.path.join(sDir, f)
        tf = os.path.join(tDir, f)
        if os.path.isfile(sf):
            if not os.path.exists(tDir):
                os.makedirs(tDir)
            open(Replace(tf), 'wb').write(Replace(open(sf, 'rb').read()))
        if os.path.isdir(sf):
            CopyFiles(sf, tf)

def Usage():
    print 'this is Usage()'
    print 'run_Name.py'
    print 'run.py Name'

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
    
    DoClean('./project/')
    CopyFiles('./template/', './project/')
