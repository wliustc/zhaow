#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# @filename:     .py
# @description:  .
# @author:       zhaow
# @created:      2015-09-21 22:52:54
# @version:      0.1
#
import sys, os, ftplib, socket

CONST_HOST = "192.168.148.19"
CONST_USERNAME = "logback"
CONST_PWD = "logback"
CONST_BUFFER_SIZE = 8192

COLOR_NONE = "\033[m"
COLOR_GREEN = "\033[01;32m"
COLOR_RED = "\033[01;31m"
COLOR_YELLOW = "\033[01;33m"


def connect():
    try:
        ftp = ftplib.FTP(CONST_HOST)
        ftp.login(CONST_USERNAME, CONST_PWD)
        return ftp
    except socket.error, socket.gaierror:
        print("FTP is unavailable,please check the host,username and password!")
        sys.exit(0)


def disconnect(ftp):
    ftp.quit()


def upload(ftp, filepath):
    f = open(filepath, "rb")
    file_name = os.path.split(filepath)[-1]
    try:
        ftp.storbinary('STOR %s' % file_name, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        return False
    return True


def download(ftp, filename):
    f = open(filename, "wb").write
    try:
        ftp.retrbinary("RETR %s" % filename, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        return False
    return True


def list(ftp):
    ftp.dir()


def find(ftp, filename):
    ftp_f_list = ftp.nlst()
    if filename in ftp_f_list:
        return True
    else:
        return False


def help():
    print("help info:")
    print("[./ftp.py l]\t show the file list of the ftp site ")
    print("[./ftp.py f filenamA filenameB]\t check if the file is in the ftp site")
    print("[./ftp.py p filenameA filenameB]\t upload file into ftp site")
    print("[./ftp.py g filenameA filenameB]\t get file from ftp site")
    print("[./ftp.py h]\t show help info")
    print("other params are invalid")


if __name__ == "__main__":
    #连接FTP
    ftp = connect()

    for lists in ftp.nlst():
        print lists

    #关闭FTP连接
    disconnect(ftp)
