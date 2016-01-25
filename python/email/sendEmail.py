# -*- coding:UTF-8 -*-
import ConfigParser
import codecs
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, server, username, password, sender, receiver, cc, title, contentPath):
        self.__server = server
        self.__username = username
        self.__password = password
        self.__sender = sender
        self.__receiver = receiver
        self.__cc = cc
        self.__title = title
        self.__contentPath = contentPath

    def getServer(self):
        return self.__server

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def getSender(self):
        return self.__sender

    def getReceiver(self):
        return self.__receiver

    def getCc(self):
        return self.__cc

    def getTitle(self):
        return self.__title

    def getContentPath(self):
        return self.__contentPath


def readConf():
    conf = ConfigParser.ConfigParser()
    conf.readfp(codecs.open('config.ini', "r", "utf-8"))
    # conf.read('config.ini')
    server = conf.get('email', 'server')
    username = conf.get('email', 'username')
    password = conf.get('email', 'password')
    sender = conf.get('email', 'from')
    receiver = conf.get('email', 'to')
    cc = conf.get('email', 'cc')
    title = conf.get('email', 'subject')
    contentPath = conf.get('email', 'contentPaht')
    email = Email(server, username, password, sender, receiver, cc, title, contentPath)
    return email


def sendMail(mail):
    msg = MIMEMultipart()
    # msg['Subject'] = Header(mail.getTitle(), 'utf-8')
    # # msg['From'] ="".join('%s<' + mail.getSender().split('<')[1]) % (Header(mail.getSender().split('<')[0], 'utf-8'))
    # # print msg['From']
    # # msg['To'] = "".join('%s<' + mail.getReceiver().split('<')[1]) % (Header( mail.getReceiver().split('<')[0], 'utf-8'))
    # print mail.getSender()
    # # msg['From'] =mail.getSender()
    # # msg['To'] =mail.getReceiver()
    # # msg['Cc'] = mail.getCc()
    # # # 邮件正文内容
    # fp = open(mail.getContentPath(), 'rb')
    # msg = MIMEText(fp.read(), _subtype='plain', _charset='utf-8')
    # fp.close()

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login('zw19882@163.com', '2996313')
    smtp.sendmail('zw19882@163.com', 'zw19881@163.com', '123')
    smtp.quit()


if __name__ == '__main__':
    mail = readConf()
    sendMail(mail)




    # msg = MIMEMultipart()
    # # att1 = MIMEText(open('C://QcOSD.txt', 'rb').read(),'base64', 'utf-8')
    # # att1["Content-Type"] = 'application/octet-stream'
    # # att1["Content-Disposition"] = 'attachment;;filename="myfile.doc"'
    # #这里的filename可以任意写，写什么名字，邮件中显示什么名字
    #
    # # msg.attach(att1)
    #
    # with open('C://QcOSD.txt', 'rb') as f:
    #     # 设置附件的MIME和文件名，这里是png类型:
    #     mime = MIMEBase('text', 'txt', filename='QcOSD.txt')
    #     # 加上必要的头信息:
    #     mime.add_header('Content-Disposition', 'attachment', filename='QcOSD.txt')
    #     mime.add_header('Content-ID', '<0>')
    #     mime.add_header('X-Attachment-Id', '0')
    #     # 把附件的内容读进来:
    #     mime.set_payload(f.read())
    #     # 用Base64编码:
    #     email.encoders.encode_base64(mime)
    #     # 添加到MIMEMultipart:
    #     msg.attach(mime)
    #
    #
    # msg['Subject'] = Header(subject, 'utf-8')
    # msg['From'] = '赵微'.decode('utf8') + '<' + sender + '>'
    # msg['To'] = receiver.decode('utf8')
    #
    #
    # smtp = smtplib.SMTP()
    # smtp.connect(smtpserver)
    # smtp.login(username, password)
    # smtp.sendmail(sender, receiver, msg.as_string())
    # smtp.quit()
