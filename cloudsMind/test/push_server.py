#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
import paramiko


# mosquitto_pub -t hello -i 123 -d -q 2 -h 111.13.139.159 -m hjhj >/opt/logs1
def excute():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('172.19.59.35', 22, username='root', password='123456', timeout=4)
        stdin, stdout, stderr = client.exec_command('ping www.baidu.com >/opt/test/'+threading.currentThread().getName()+'.log')
        # for std in stdout.readlines():
        #     print std,
    except Exception,e:
        print "[-] excute fail :" +str(e)

if __name__ == '__main__':


    threads=[]
    print 'begin'
    threading_num = 2
    # s = threading.Semaphore(threading_num)
    for i in range(1,threading_num+1):
        t = threading.Thread(target=excute)
        t.getName()
        threads.append(t)
    for t in threads:
        # time.sleep(ThinkTime)
        # print "thread %s" %t #打印线程
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print "Exiting Main Thread"



