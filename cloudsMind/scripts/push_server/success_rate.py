#!/usr/bin/python
# -*- coding:utf-8 -*-

import paramiko
#
# @filename:     success.py
# @description:  统计总共接收的消息的成功率,及响应时间
# @author:       zhaow
# @created:      2015-12-28
# @version:      0.1
#

def excute():
    filename=[]
    rows=0
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.0.245', 22, username='root', password='ngem1688', timeout=4)
        stdin, stdout, stderr = client.exec_command('ls -l /opt/test')
        for std in stdout.readlines():
            if 'Thread' in std:
                file=std.split(' ')[-1]
                filepath='/opt/test/'+file
                filename.append(filepath)
                stdin, stdout, stderr=client.exec_command('wc -l '+filepath+'')#'wc -l '+filepath+''
                rows+=int(stdout.read().split(' ')[0])
        print len(filename)
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