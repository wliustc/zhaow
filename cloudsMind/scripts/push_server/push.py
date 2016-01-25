#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import paramiko


#
# @filename:     push.py
# @description:  push消息
# @author:       zhaow
# @created:      2015-12-28
# @version:      0.1
#

# mosquitto_pub -t hello -i 123 -d -q 2 -h 111.13.139.159 -m hjhj >/opt/logs1
# mosquitto_sub -h 111.13.139.159 -t hello -q 2
def excute():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('172.19.59.35', 22, username='root', password='123456', timeout=4)
        tdin, stdout, stderr = client.exec_command('mosquitto_pub -t hello -i 123 -d -q 2 -h 111.13.139.159')
        for std in stdout.readlines():
            print std,
    except Exception, e:
        print "[-] excute fail :" + str(e)


if __name__ == '__main__':
    # 执行次数
    num = 100
    starttime = datetime.datetime.now()
    for i in range(1, num + 1):
        # time.sleep(ThinkTime)
        excute()
    print '开始时间：%s' % starttime
    print "xiting Main Thread"
