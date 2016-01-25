#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     push_agent.py
# @description: 执行stresspush.py脚本，向redis发送数据，并验证redis中接收数据量与发送是否相同
# @author:       zhaow
# @created:      2016-01-06
# @version:      0.1
#
import ConfigParser
import paramiko
import redis


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


def insertData():
    c = push_key()
    ip = read_conf('PushAgent', 'IP')
    username = read_conf('PushAgent', 'UserName')
    port = read_conf('PushAgent', 'Port')
    total = read_conf('PushAgent', 'Total')
    c.connect(ip, int(port), username, pkey=k)
    print "连接到PushAgent ：%s" % (ip)
    stdin,stdout,stderr=c.exec_command('/root/stresspush.py')
    print stdout.read()
    # 连接redis
    redisIp = read_conf('Redis', 'IP')
    redisPort = read_conf('Redis', 'Port')
    r = redis.Redis(host=redisIp, port=int(redisPort), db=0)
    length = r.llen('CPS.QUEUE.ANDROID')
    # 验证redis中数据是否与发送相符
    if length == int(total):
        print '共发送了 %s 条数据' % (total)


def main():
    insertData()

if __name__ == '__main__':
    main()
