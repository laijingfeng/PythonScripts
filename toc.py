#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os, os.path, sys
import shutil,datetime

top_level=77
lnk_temp='%s- [%s](#%s)'
TOC='#### Contents'

def generate_toc_dir(dir_name):
    for parent, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            if filename.find('.md') != -1:
                print 'file:' + parent + '\\' + filename
                generate_toc(parent + '\\' + filename)

def generate_toc(fname):
    global top_level
    lines = []
    with open(fname, 'r') as file:
        lines = file.readlines()
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    destf= '.'.join((fname,ts,'bak'))
    shutil.copy(fname, destf)
    print "Backup was created: [%s]"%destf

    lines = pre_work(lines)
    
    headers = [e.strip() for e in lines if re.match(r'#+', e)]
    #find top_level
    for i,h in enumerate(headers):
        ln = len(re.search(r'^#+',h).group(0))
        top_level = ln if ln < top_level else top_level
        headers[i] = re.sub(r'^#+\s*', str(ln)+' ', h)
    headers = [tr_header(h) for h in headers]
    with open(fname,'w') as f:
        f.write(TOC + '\n')
        f.write('\n'.join(headers) + '\n\n')
        f.write(''.join(lines))

def pre_work(lines):
    # delete old Contents
    
    s_id, e_id, idx = -1, -1, 0
    for e in lines:
        if e.find(TOC) != -1:
            s_id = idx
            e_id = s_id
        elif s_id != -1 and e.find('#') != -1:
            e_id = idx
        elif s_id != -1 and e.find('#') == -1:
            break;
        idx = idx + 1

    if s_id != -1:
        lines[s_id:e_id - s_id + 1] = []

    # delete blank lines before article

    blankLineCnt = 0
    idx = 0
    for e in lines:
        if idx == blankLineCnt and e == '\n':
            blankLineCnt = blankLineCnt + 1
        else:
            break
        idx = idx + 1
        
    if blankLineCnt != 0:
        lines[0:blankLineCnt] = []

    return lines

def tr_header(header):
    global lnk_temp
    lvl, txt = re.findall(r'^(\d+) (.*)', header)[0]
    return lnk_temp%((int(lvl)-top_level)*'    ', txt, re.sub(' ','-',re.sub('[^-a-z0-9 ]','',txt.lower())))

def usage():
    print '---------usage---------'
    print 'python toc.py <markdown file name | dir name>'
    print 'Example: python toc.py README.md'
    print 'Example: python toc.py lai'
    print '=========usage========='

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        usage()
        exit()
    
    infile = sys.argv[1]
    if infile.find('.md') != -1:
        generate_toc(infile)
    else:
        generate_toc_dir(infile)
