#!/usr/bin/python
# -*- coding:utf-8 -*-

import paramiko
import time
#
# @filename:     success.py
# @description:  统计总共接收的消息的成功率,及响应时间
# @author:       zhaow
# @created:      2015-12-28
# @version:      0.1
#

def excute():
    filelist=[]
    rows=0
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('172.19.59.35', 22, username='root', password='123456', timeout=4)
        stdin, stdout, stderr = client.exec_command('ls -l /opt/test')
        for std in stdout.readlines():
            if 'Thread' in std:
                file=std.split(' ')[-1]
                filepath='/opt/test/'+file
                filelist.append(filepath)
        for f in filelist:
            stdin1, stdout1, stderr1=client.exec_command('stat '+filepath+'')#'wc -l '+filepath+''
            for s in stdout1.readlines():
                if 'Modify' in s:
                    t=s.split(' ')[1:3]

        print len(filelist)
        return rows
    except Exception,e:
         print "[-] excute fail :" +str(e)


if __name__ == '__main__':
    # threadNum=100  #客户端数
    # num=1000         #通信次数
    total=10000 #并发数*迭代轮次
    rows=excute()
    rate=float(rows*100)/float(total)
    print '成功率： %s'% rate+'%'