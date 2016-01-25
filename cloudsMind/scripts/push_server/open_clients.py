#!/usr/bin/python
# -*- coding:utf-8 -*-

#
# @filename:     open_client.py
# @description:  控制打开的客户端数量
# @author:       zhaow
# @created:      2015-12-28
# @version:      0.1
#
import threading
import paramiko

# mosquitto_pub -t hello -i 123 -d -q 2 -h 111.13.139.159 -m hjhj >/opt/logs1
#mosquitto_sub -h 111.13.139.159 -t hello -q 2
def excute(i):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.0.245', 22, username='root', password='ngem1688', timeout=4)
        client.exec_command('mosquitto_sub -t aaabbbcccdddeeefffggg'+i+' -q 2 -p 9883 >/opt/test/'+threading.currentThread().getName()+'bb'+i+'aa'+i+'d.log')
    except Exception,e:
        print "[-] excute fail :" +str(e)

if __name__ == '__main__':
    threads=[]
    print 'begin'
    # for m in range(1,101):
    threading_num = 10000
    for i in range(1,threading_num+1):
        t = threading.Thread(target=excute,args=(str(i),))
        t.getName()
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    # for t in threads:
        t.join()
    print "Exiting Main Thread"