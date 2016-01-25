#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     push_client.py
# @description:针对集群开启多个客户端
# @author:       zhaow
# @created:      2016-01-06
# @version:      0.1
#
import ConfigParser
import threading
import paramiko
import time


def read_conf(section, key):
    config = ConfigParser.ConfigParser()
    config.read('conf/conf.ini')
    return config.get(section, key)


def push_key():
    global k
    k = paramiko.RSAKey.from_private_key_file('conf/emm-push-key.pem')
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return c


def pushClient_Start():
    c = push_key()
    ipCluster = read_conf('Client', 'IPCluster')
    username = read_conf('Client', 'UserName')
    port = read_conf('Client', 'Port')
    clients=read_conf('Client','Clients')

    client=int(clients)
    dic = eval(ipCluster)
    for key in dic.keys():
        for ip in dic.get(key).split(','):
            c.connect(ip, int(port), username, pkey=k)
            print '开启 %s 服务器的Client' % (ip)
            c.exec_command(
                'cd /home/ubuntu/emqtt_benchmark-master ;/home/ubuntu/emqtt_benchmark-master/emqtt_bench_sub -h  ' + key + '  -c '+client+' -t abcdefghijklmnopqrst/%i -i 2 -q 0  >/home/ubuntu/client' +
                ip + '.log')
        c.close()


def connectClient(ip, username, port, clients):
    c = push_key()
    c.connect(ip, int(port), username, pkey=k)
    time.sleep(5)
    stdin, stdout, stderr = c.exec_command('tail -1 /home/ubuntu/client' + ip + '.log')
    lines = stdout.read()
    list = []
    for line in lines.splitlines():
        list.append(line)
    print '%s     %s' % (ip, list[-1])
    if str(int(clients) - 1) in list[-1]:
        print '%s 客户端连接初始化完成' % (ip)
        c.close()
    else:
        c.close()
        time.sleep(3)
        connectClient(ip, username, port, clients)


def openThreads():
    ip = read_conf('Client', 'IPtotal')
    username = read_conf('Client', 'UserName')
    port = read_conf('Client', 'Port')
    num = read_conf('Client', 'num')
    clients = read_conf('Client', 'Clients')
    ipList = []
    for IP in ip.split(','):
        ipList.append(IP)
    threads = []
    print 'begin'
    # threading_num = int(num)
    threading_num = len(ipList)
    for i in range(0, threading_num):
        t = threading.Thread(target=connectClient, args=(ipList[i], username, port, clients))
        t.getName()
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print "Exiting Main Thread"


def main():
    pushClient_Start()
    time.sleep(5)
    openThreads()


if __name__ == '__main__':
    main()
