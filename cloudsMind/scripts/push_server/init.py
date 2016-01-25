#!/usr/bin/python
# -*- coding:utf-8 -*-

import paramiko

#
# @filename:     init.py
# @description:  初始化,删除日志文件，及kill掉所有相关进程
# @author:       zhaow
# @created:      2015-12-28
# @version:      0.1
#

# mosquitto_pub -t hello -i 123 -d -q 2 -h 111.13.139.159 -m hjhj >/opt/logs1
def excute():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.0.245', 22, username='root', password='ngem1688', timeout=4)
        client.exec_command('rm -rf /opt/test/*')
        client.exec_command('killall mosquitto_sub')
        client.exec_command('mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf -d')

    except Exception,e:
        print "[-] excute fail :" +str(e)

if __name__ == '__main__':
    excute()