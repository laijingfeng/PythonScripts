#!/usr/bin/python
#-*-coding:utf-8-*-
# version: 2018-01-22 14:48:44
"""get mail"""

import sys
import os
import imaplib
import email
import threading
import time
import codecs
import json
from collections import OrderedDict
import xlrd

class MainClass(object):
    """main class"""
    def __init__(self):
        """init the class"""
        self.enter_cwd_dir = ''
        self.python_file_dir = ''
    def parse_arg(self):
        """parse input args"""
        if len(sys.argv) < 1:
            return False, None
        return True, sys.argv
    def get_exe_path(self, simple_path):
        """get the direct path"""
        return os.path.join(self.enter_cwd_dir, self.python_file_dir, simple_path)
    def usage(self):
        """just the usage description of this code"""
        print 'this is usage()'
    def run(self):
        """enter the class"""
        success, args = self.parse_arg()
        if not success:
            self.usage()
            exit(-1)
        self.enter_cwd_dir = os.getcwd()
        self.python_file_dir = os.path.dirname(sys.argv[0])
        self.work()
    def get_mail(self):
        """get mail return whether has new mail"""
        ret = False
        mail_host = 'imap.exmail.qq.com'
        mail_user = 'laijf@myjooy.com'
        mail_pass = 'Lai123'
        server = imaplib.IMAP4_SSL(mail_host, 993)
        server.login(mail_user, mail_pass)
        server.select()
        res, data = server.search(None, 'unseen')
        if res == 'OK' and data[0] != '':
            print 'have new mail'
            mail_id = data[0].split()[0]
            msg_content = server.fetch(mail_id, '(RFC822)')
            msg = email.message_from_string(msg_content[1][0][1])
            ret = self.parse_mail(msg)
            server.store(mail_id, '+FLAGS', '\\seen')
        else:
            print 'query error or no new mail'
        return ret
    def parse_mail(self, msg):
        """parse mail"""
        ret = False
        for part in msg.walk():
            if not part.is_multipart():
                file_name = part.get_filename()
                if file_name:
                    data = part.get_payload(decode=True)
                    self.save_file(data, './', file_name)
                    ret = True
        return ret
    def save_file(self, data, path, filename):
        """save file"""
        file_path = path + filename
        with open(file_path, 'wb') as file_handler:
            file_handler.write(data)
    def upload_to_ftp(self):
        """upload files to ftp"""
        pass
    def clean(self):
        """clean files"""
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and (filename.startswith('~') is False):
                if filename.endswith('.xlsx') or filename.endswith('.json'):
                    os.remove(filename)
    def excel_to_json(self):
        """excel to json return whether success"""
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and filename.endswith('.xlsx') and (filename.startswith('~') is False):
                convert_list = []
                work_book = xlrd.open_workbook(filename)
                sheet = work_book.sheet_by_index(0)
                title = sheet.row_values(0)
                data_type = sheet.row_values(1)
                for row_num in range(3, sheet.nrows):
                    row_value = sheet.row_values(row_num)
                    single = OrderedDict()
                    for col_num in range(0, len(row_value)):
                        if data_type[col_num] == 'string':
                            single[title[col_num]] = str(row_value[col_num]).replace('.0', '')
                        elif data_type[col_num] == 'int':
                            single[title[col_num]] = int(row_value[col_num])
                        else:
                            single[title[col_num]] = row_value[col_num]
                    convert_list.append(single)
                j = json.dumps(convert_list)
                with codecs.open(filename.replace('.xlsx', '.json'), 'w', 'utf-8') as file_handler:
                    file_handler.write(j)
    def work(self):
        """do real work"""
        self.clean()
        return
        if self.get_mail() is True:
            self.excel_to_json()
            self.upload_to_ftp()
            self.clean()

class MyThread(threading.Thread):
    """my thread"""
    def run(self):
        get_mail = MainClass()
        while True:
            get_mail.run()
            time.sleep(5)

if __name__ == '__main__':
    #GET_MAIL_THREAD = MyThread()
    #GET_MAIL_THREAD.start()
    GET_MAIL = MainClass()
    GET_MAIL.run()
