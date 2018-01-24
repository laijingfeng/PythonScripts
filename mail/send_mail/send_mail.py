#!/usr/bin/python
#-*-coding:utf-8-*-
# version: 2018-01-22 14:48:44
"""send mail"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

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
    def send_mail(self):
        """send mail"""
        mail_host = 'smtp.exmail.qq.com'
        mail_user = 'laijf@myjooy.com'
        mail_pass = 'Lai123'
        receiver = ['laijf@myjooy.com']
        message = MIMEMultipart()
        message['From'] = Header('Jerrylai', 'utf-8')
        message['To'] = Header('Jerrylai', 'utf-8')
        message['Subject'] = Header('H5Table', 'utf-8')
        message.attach(MIMEText('H5Table', 'plain', 'utf-8'))
        has_att1 = False
        files = os.listdir('./')
        for filename in files:
            if os.path.isfile(filename) and (filename.startswith('~') is False):
                if filename.endswith('.xlsx'):
                    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
                    att1["Content-Type"] = 'application/octet-stream'
                    att1["Content-Disposition"] = 'attachment; filename="' + filename +'"'
                    message.attach(att1)
                    has_att1 = True
        if has_att1 is True:
            try:
                smtp_object = smtplib.SMTP_SSL(mail_host, 465)
                smtp_object.login(mail_user, mail_pass)
                smtp_object.sendmail(mail_user, [receiver,], message.as_string())
                smtp_object.quit()
                print 'send success'
                return True
            except smtplib.SMTPException:
                print 'send error'
                return False
        else:
            print 'no excel file'
            return False
    def work(self):
        """do real work"""
        self.send_mail()

if __name__ == '__main__':
    MAIN_CLASS = MainClass()
    MAIN_CLASS.run()
