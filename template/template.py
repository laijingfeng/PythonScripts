#!/usr/bin/python
#-*-coding:utf-8-*-
# version: 2018-01-22 14:48:44
"""code template"""

import sys
import os
import json
import email
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import imaplib

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
    def send_mail(self, msg):
        """send mail"""
        mail_host = 'smtp.exmail.qq.com'
        mail_user = 'laijf@myjooy.com'
        mail_pass = 'Lai123'
        receiver = 'laijf@myjooy.com'
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = formataddr(["Jerrylai", mail_user])
        message['To'] = formataddr(['Jerrylai', receiver])
        message['Subject'] = '《开心斗舞》音乐配置表'
        try:
            smtp_object = smtplib.SMTP_SSL(mail_host, 465)
            smtp_object.login(mail_user, mail_pass)
            smtp_object.sendmail(mail_user, [receiver,], message.as_string())
            smtp_object.quit()
            return True
        except smtplib.SMTPException:
            return False
    def get_mail(self):
        """get mail"""
        mail_host = 'imap.exmail.qq.com'
        mail_user = 'laijf@myjooy.com'
        mail_pass = 'Lai123'
        server = imaplib.IMAP4_SSL(mail_host, 993)
        server.login(mail_user, mail_pass)
        server.select()
        res, data = server.search(None, 'unseen')
        print data
        if res == 'OK' and data[0] != '':
            mail_id = data[0].split()[0]
            print mail_id
            print 'have new mail'
            msg_content = server.fetch(mail_id, '(RFC822)')
            #print msg_content
            msg = email.message_from_string(msg_content[1][0][1])
            content = msg.get_payload(decode=True)
            print content
            #server.store(mail_id, '+FLAGS', '\\seen')  # 标记已读
        else:
            print 'query error or no new mail'
    def work(self):
        """do real work"""
        #with open(self.get_exe_path('./config.json'), 'r') as read_file:
        #    config = json.load(read_file)
        #test_name = config['test_name']
        #test_age = config['test_age']
        #print test_name, test_age
        #self.send_mail('你好')
        self.get_mail()

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
